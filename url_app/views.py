from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import ShortenForm
from .models import ShortURL
from .utils import generate_code


def index(request):
    """Home page with form and list of recent short URLs."""
    shortened_url = None

    if request.method == 'POST':
        form = ShortenForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['url']
            # Optional: basic allowlist check for redirection safety (usually fine to allow any HTTP/HTTPS)
            if not (target.startswith('http://') or target.startswith('https://')):
                form.add_error('url', 'URL must start with http:// or https://')
            else:
                # Try to find existing mapping to avoid duplicates
                obj = ShortURL.objects.filter(original_url=target).first()
                if not obj:
                    with transaction.atomic():
                        # Ensure unique short_code
                        for length in (7, 8, 9, 10):
                            code = generate_code(length)
                            if not ShortURL.objects.filter(short_code=code).exists():
                                obj = ShortURL.objects.create(original_url=target, short_code=code)
                                break
                        if not obj:
                            raise RuntimeError("Failed to generate a unique short code.")
                # Build absolute URL for display
                base = getattr(settings, 'SITE_BASE_URL', request.build_absolute_uri('/').rstrip('/'))
                shortened_url = f"{base}/{obj.short_code}"
    else:
        form = ShortenForm()

    recent = ShortURL.objects.order_by('-created_at')[:10]
    return render(request, 'index.html', {
        'form': form,
        'shortened_url': shortened_url,
        'recent': recent,
    })


def follow(request, code: str):
    """Redirect /<code> to its original_url and increment clicks."""
    obj = ShortURL.objects.filter(short_code=code).first()
    if not obj:
        raise Http404("Short code not found")
    ShortURL.objects.filter(pk=obj.pk).update(clicks=obj.clicks + 1)
    return HttpResponseRedirect(obj.original_url)
