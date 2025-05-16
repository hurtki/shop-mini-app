from multiprocessing import cpu_count
from os import environ

def max_workers():
    """
    Calculate the maximum number of workers based on the number of CPU cores.
    """
    return cpu_count()

bind = "0.0.0.0:" + environ.get("PORT", "8000")
max_requests = 1000
worker_class = "gevent"
workers = max_workers()

env = {
    'Django_SETTINGS_MODULE': 'shop_tg_app.settings',
}


reload = True
name = "shop_tg_app"
