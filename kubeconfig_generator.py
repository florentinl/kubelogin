from certificate_generator import get_cert_and_key
import yaml


def get_kube_config(username, cluster_name, api_url):
    key, cert, ca = get_cert_and_key(username)
    kubeconfig = {'apiVersion': 'v1',
                  'clusters': [{'cluster':
                                {'certificate-authority-data': ca,
                                 'server': api_url},
                                'name': cluster_name}],
                  'contexts': [{'context': {'cluster': cluster_name,
                                            'namespace': 'default',
                                            'user': username},
                                'name': f'{username}@{cluster_name}'}],
                  'current-context': f'{username}@{cluster_name}',
                  'kind': 'Config',
                  'preferences': {},
                  'users': [{'name': username,
                             'user': {'client-certificate-data': cert,
                                      'client-key-data': key}}]}
    dump = yaml.dump(kubeconfig)
    return dump