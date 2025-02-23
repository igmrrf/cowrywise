from pybreaker import CircuitBreaker
import requests
import os
from .errors import LibraryError

# Get the URL from environment variable
FRONTEND_API_URL = os.getenv('FRONTEND_API_URL', 'http://localhost:3000')

sync_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60
)

@sync_breaker
def sync_with_frontend_service(action, data):
    try:
        response = requests.post(f'{FRONTEND_API_URL}/sync/books', json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise LibraryError(f"Failed to sync with frontend service: {str(e)}", 503)