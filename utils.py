# Bu kod utils.py içindir
# filepath: görüntü/utils.py

import time

def debounce(wait_time):
    """
    Fonksiyon çağrıları arasında minimum süre olmasını sağlar.
    """
    def decorator(fn):
        last_time = [0]
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_time[0] > wait_time:
                last_time[0] = current_time
                return fn(*args, **kwargs)
        return wrapper
    return decorator

def clamp(value, min_value, max_value):
    """
    Bir değeri belirli bir aralıkta sınırlar.
    """
    return max(min_value, min(value, max_value))