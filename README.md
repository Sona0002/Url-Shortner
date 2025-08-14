Django URL Shortener 

Overview

A simple Django-based URL shortener with a clean web interface.

How it works:

User enters a long URL in the form.

The app validates the URL format (must start with http:// or https://).

If a shortened code for that URL already exists, it reuses it.

Otherwise, it generates a unique random short code and saves it with the original URL.

The short link is displayed (e.g., http://127.0.0.1:8000/abc1234).

Visiting the short link redirects the browser to the original URL and increments its click count.
