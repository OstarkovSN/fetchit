import json
from itertools import cycle
from tenacity import (
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    wait_fixed
)
from openai import (
    APIConnectionError,
    RateLimitError,
    Timeout,
)

MAPPING = {
    "stop_after_attempt": stop_after_attempt,
    "wait_exponential": wait_exponential,
    "wait_fixed": wait_fixed,
    "retry_if_exception_type": retry_if_exception_type,
    "tuple": tuple,
    "APIConnectionError": APIConnectionError,
    "RateLimitError": RateLimitError,
    "Timeout": Timeout
}

try:
    with open('secrets.json', encoding='utf-8') as file:
        secrets = json.load(file)
except FileNotFoundError:
    secrets = {}

ITERABLES_MAPPING = {
    
}

ITERABLES_MAPPING.update(secrets)

for key, value in ITERABLES_MAPPING.items():
    ITERABLES_MAPPING[key] = cycle(value)