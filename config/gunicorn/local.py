wsgi_app = "config.wsgi:application"
loglevel = 'debug'
workers = 1
bind = '0.0.0.0:8000'
reload = True
# accesslog = errorlog = '/var/log/gunicorn/zerodev_backend_dev.log'
capture_output = True
# pidfile = '/var/run/gunicorn/dev.pid'
# daemon = True


# kill $(cat /var/run/gunicorn/zerodev_backend_dev.pid)
# gunicorn -c config/gunicorn/dev.py config.wsgi
