# Deployment workflow

The streamlit app is deployed to the Labs GKE cluster through [Helm](https://helm.sh/). The Helm chart is located in the [`helm`](./helm/) directory.

The deployment workflow is defined in the [`.github/workflows/build_and_deploy.yaml`](../.github/workflows/build_and_deploy.yaml) file. It is triggered on push to the `main` branch. First the docker image is built and pushed to Github Container Registry. Then, the Helm chart is deployed to the GKE cluster.

The [`llllm-contacts` ConfigMap](./k8s/configmap.yaml) is used to store the contact details of the team members responsible for the app.
