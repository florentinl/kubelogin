from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

rbac = client.RbacAuthorizationV1Api()


def get_role_binding_list():
    rbac = client.RbacAuthorizationV1Api()
    role_bindings = rbac.list_namespaced_role_binding("default").items
    def get_name(cluster_role): return cluster_role.metadata.name
    return list(map(get_name, role_bindings))


def role_binding_exists(name):
    username = "viarezo:" + name
    return username in get_role_binding_list()


def build_role_binding(name):
    username = "viarezo:" + name
    metadata = client.V1ObjectMeta(name=username, namespace="default")
    role_ref = client.V1RoleRef(
        api_group="rbac.authorization.k8s.io", kind="ClusterRole", name="viarezo-team")
    subject = client.V1Subject(
        api_group="rbac.authorization.k8s.io", kind="User", name=username)
    return client.V1RoleBinding(metadata=metadata, role_ref=role_ref, subjects=[subject])


def create_role_binding(name):
    cluster_role = build_role_binding(name)
    rbac.create_namespaced_role_binding(namespace="default", body=cluster_role)
