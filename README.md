# Kubelogin

Kubelogin is a simple backend server that allows you to generate a kubeconfig file for a Kubernetes cluster using OAuth2 authentication.

Kubelogin is used for training sessions where a user needs to access a Kubernetes cluster with a limited set of permissions. Currently it creates a dedicated namespace for the user in which he has unlimited access. And grants him read-only access to the rest of the cluster so he can explore it and see demos.

This project was more of a motivation to get familiar with OAuth2 authorization and Kubernetes RBAC than a real-world solution. Although it works there are most likely a lot of security issues with it as well as some rough edges.

## Installation

It can be deployed using helm although the helm chart relies on cert-manager and Traefik so it might not match your setup. Additionally many values must be changed to fit your needs and some parameters within the python code must also be changed.
