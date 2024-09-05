workers = 8
bind = '0.0.0.0:8000'
wsgi_app = 'upsmanager.wsgi'
secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
reload = True
