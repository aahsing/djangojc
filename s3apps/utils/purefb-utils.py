import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import functools


# Find the latest API version, we use version 2.x.
def get_api_version(cluster_name):
    retry_strategy = Retry(
        total=3,  # maximum number of retries
        backoff_factor=1,  # factor by which to increase the sleep time between retries
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    base_url = 'https://{}/api/api_version'.format(cluster_name)
    headers = {'Content-Type': 'application/json'}
    http = requests.Session()
    http.mount("https://", adapter)
    try:
        response = http.get(base_url, headers=headers, verify=False, timeout=30)
        # Raises an exception if the HTTP status code is not in 2xx range.
        response.raise_for_status()

        versions_list = response.json()['versions']
        # Return the latest version
        return versions_list[len(versions_list) - 1]

    except requests.exceptions.HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
    except requests.exceptions.ConnectionError as connection_error:
        print(f'Connection error occurred: {connection_error}')
    except requests.exceptions.Timeout as timeout_error:
        print(f'Timeout error occurred: {timeout_error}')
    except requests.exceptions.RequestException as request_error:
        print(f'An error occurred: {request_error}')


"""
The Pure FB REST API accepts API tokens generated from array or OAuth access token created by an authorized server.
We use API token to interact with Pure FB API here.
"""
def generate_api_token():
    pass


# Using the API token to generate the auth token which will be used to the following request
def get_auth_token(cluster, api_token):
    session = requests.Session()
    headers = {'api-token': f'{api_token}'}
    print(headers)
    request_url = 'https://{}/api/login'.format(cluster)
    response = session.post(request_url, headers=headers, verify=False)
    return response.headers


if __name__ == '__main__':
    cluster = '10.23.33.50'
    api_version = get_api_version(cluster)
    api_token = 'T-57bfb519-5859-4b9e-b997-feff692aa592'
    response = get_auth_token(cluster, api_token)
    print(response['x-auth-token'])

