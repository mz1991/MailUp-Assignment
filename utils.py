""" Import requests to make HTTP requests"""
import requests
import json

def do_post(post_url, post_data=None, post_header=None, rest_client_obj=None):
    """ Execute HTTP POST"""
    try:
        if post_data:
            http_response = requests.post(post_url, data=json.dumps(post_data), headers=post_header)
        else:
            http_response = requests.post(post_url, headers=post_header)
        if http_response.status_code == 401:
            # Refresh the Token
            rest_client_obj.get_auth_token(refresh_token_post=True)
            return do_post(post_url, post_data, post_header, rest_client_obj)
        else:
            return http_response
    except Exception as exception:
        raise exception

def do_get(get_url, get_header, rest_client_obj=None):
    """ Execute HTTP GET"""
    try:
        http_response = requests.get(get_url, headers=get_header)
        if http_response.status_code == 401:
            # Refresh the Token
            rest_client_obj.get_auth_token(refresh_token_post=True)
            return do_get(get_url, get_header, rest_client_obj)
        else:
            return http_response
    except Exception as exception:
        raise exception

def buid_auth_header(access_token):
    """Return the http auth header"""
    auth_token = 'Bearer {}'.format(access_token)
    headers = {}
    headers["Authorization"] = auth_token
    headers["Content-Type"] = 'application/json'
    return headers
