import pytest
from decorator import decorator

current_report = {}

def get_current_report():
    return current_report


def ai_metric(threshold=0.5, *args, **kwargs):
    name = kwargs['name']
    def ai_metric_dec(func, *args, **kwargs):
        # Add functionality before the original function call
        metric = func(*args, **kwargs)
        # Add functionality after the original function call
        current_report[name] = metric
        assert metric >= threshold
    return decorator(ai_metric_dec)