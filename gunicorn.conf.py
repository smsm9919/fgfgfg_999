# gunicorn.conf.py
workers = 2
threads = 4
preload_app = True
bind = "0.0.0.0:" + __import__("os").environ.get("PORT", "10000")
timeout = 180
max_requests = 1000
max_requests_jitter = 100
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}