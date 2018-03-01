import logging, requests
from utils import validate_basic_params

log = logging.getLogger()

"""
Get detail of the asset with the specified IP address.
@return a dictionary of asset details
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param asset_ip: IP address of the asset to get.
"""
def get_asset_detail(cluster_name, username, api_key, asset_ip):
    validate_basic_params(cluster_name, username, api_key)
    if not asset_ip:
        log.error('Asset IP not specified')
        raise ValueError('asset_ip is is required')
    url = 'https://%s/api/asset/ip/%s' % (cluster_name, asset_ip)
    response = requests.get(url, params={'username': username, 'api_key': api_key}, verify=False)
    response.raise_for_status()
    return response.json()

"""
Update the metadata associated with an asset.
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param asset_ip: IP address of the asset to update.
@param metadata_dict: The dictionary of metadata properties to update. New properties will be added, and exisiting properties overwritten.
@param section_name: Optional. If specified, the metadata updated will be applied to this subsection, rather than at the top level.
"""
def update_metadata(cluster_name, username, api_key, asset_ip, metadata_dict, section_name=None):
    validate_basic_params(cluster_name, username, api_key)
    if not asset_ip or not metadata_dict:
        log.error('asset_ip or metadata_dict not specified')
        raise ValueError('asset_ip and metadata_dict are required')
    url = 'https://%s/api/asset/%s/metadata' % (cluster_name, asset_ip)
    if section_name: url = 'https://%s/api/asset/%s/metadata/section/%s' % (cluster_name, asset_ip, section_name)
    response = requests.put(url, params={'username': username, 'api_key': api_key}, json=metadata_dict, verify=False)
    response.raise_for_status()

"""
Delete the specified metadata for an asset. If neither section_name nor key is specified, then all associated metadata is
deleted. If only section_name is specified, then that section of metadata is removed in it's entirety. If only key is specified,
then that top-level property is removed.
@param cluster_name: The name of your cluster, i.e. customer.portal.jask.io
@param username: The username to use when authenticating to Trident.
@param api_key: API key used to authenticate the specified username.
@param asset_ip: IP address of the asset to update.
@param section_name: Optional. The name of the metadata section to delete.
@param key: Optional. The name of the metadata key to delete.
"""
def delete_metadata(cluster_name, username, api_key, asset_ip, section_name=None, key=None):
    validate_basic_params(cluster_name, username, api_key)
    if not asset_ip:
        log.error('Asset IP not specified')
        raise ValueError('asset_ip is is required')
    url = 'https://%s/api/asset/%s/metadata' % (cluster_name, asset_ip)
    if section_name and key:
        url += '/%s/%s' % (section_name, key)
    elif section_name:
        url += '/section/' + section_name
    elif key:
        url += '/' + key
    response = requests.delete(url, params={'username': username, 'api_key': api_key}, verify=False)
    response.raise_for_status()
