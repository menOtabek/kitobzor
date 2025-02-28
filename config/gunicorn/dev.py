import multiprocessing

wsgi_app = 'config.wsgi:application'
bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count() * 2 + 1

worker_connections = 1000

worker_class = "sync"

loglevel = "info"

proc_name = "smart_ride_project"

accesslog = "/var/log/gunicorn/proc_name_access.log"  # Mijoz so'rovlari log fayli
errorlog = "/var/log/gunicorn/proc_name_error.log"  # Xatoliklar log fayli

reload = False
