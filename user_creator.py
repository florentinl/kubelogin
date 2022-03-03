from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_incluster_config()

rbac = client.RbacAuthorizationV1Api()
core_v1 = client.CoreV1Api()


def get_role_binding_list(namespace):
    rbac = client.RbacAuthorizationV1Api()
    role_bindings = rbac.list_namespaced_role_binding(namespace).items
    def get_name(cluster_role): return cluster_role.metadata.name
    return list(map(get_name, role_bindings))


def create_namespace(namespace):
    body = client.V1Namespace(
        metadata=client.V1ObjectMeta(
            name=namespace, labels={"type": "formation"}))
    core_v1.create_namespace(body=body)


def role_binding_exists(name, namespace):
    username = "viarezo:" + name
    return username in get_role_binding_list(namespace)


def build_role_binding(name, namespace):
    username = "viarezo:" + name
    metadata = client.V1ObjectMeta(name=username, namespace=namespace)
    role_ref = client.V1RoleRef(
        api_group="rbac.authorization.k8s.io", kind="ClusterRole", name="cluster-admin")
    subject = client.V1Subject(
        api_group="rbac.authorization.k8s.io", kind="User", name=username)
    return client.V1RoleBinding(metadata=metadata, role_ref=role_ref, subjects=[subject])


def create_role_binding(name, namespace):
    cluster_role = build_role_binding(name, namespace)
    rbac.create_namespaced_role_binding(namespace=namespace, body=cluster_role)
