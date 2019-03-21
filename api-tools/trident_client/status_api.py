from .utils import get_simple_list, validate_basic_params

"""
Get a list of the sensors associated with this cluster.
@return a list of the sensors associated with this cluster
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
"""
def list_sensors(cluster_name, username, api_key):
    validate_basic_params(cluster_name, username, api_key)
    url = 'https://%s/api/sensor' % cluster_name
    return get_simple_list(url, username, api_key)

"""
Get a list of active users associated with this cluster.
@return a list of active users associated with this cluster
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
"""
def list_users(cluster_name, username, api_key):
    validate_basic_params(cluster_name, username, api_key)
    url = 'https://%s/api/user' % cluster_name
    return get_simple_list(url, username, api_key)
