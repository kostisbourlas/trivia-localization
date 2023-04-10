import requests


def print_auth_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Invalid credentials")
            elif e.response.status_code == 403:
                print("You do not have permission to access this resource")
            else:
                raise
    return wrapper
