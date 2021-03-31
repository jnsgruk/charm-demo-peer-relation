## Demonstration Charm

This charm is a demonstration of the new Sidecar Charm pattern for Juju 2.9. It uses [Pebble](https://github.com/canonical/pebble) and the [Python Operator Framework](https://pythonoperatorframework.io). The charm serves little real purpose, but demonstrates how peer relations are used.

At present, this charm cannot be published to Charmhub, so you will need to build it locally. To setup a local test environment with [MicroK8s](https://microk8s.io), do the following:

```bash
$ sudo snap install --classic microk8s
$ sudo useradd -aG microk8s $(whoami)
$ sudo microk8s enable storage dns
$ sudo snap alias microk8s.kubectl kubectl
$ newgrp microk8s
```

Next install Charmcraft and build the Charm

```bash
# Install Charmcraft
$ sudo snap install charmcraft --edge

# Clone an example charm
$ git clone https://github.com/jnsgruk/charm-demo-peer-relation
# Build the charm
$ cd charm-demo-peer-relation
$ charmcraft build
```

Now you're ready to deploy the Charm:

```bash
# For now, we require the 2.9/edge channel until features land in candidate/stable
$ sudo snap refresh juju --channel=2.9/edge
# Create a model for our deployment
$ juju add-model peer-demo

# Deploy!
$ juju deploy ./peer-relation-demo.charm --resource demo-image=google/pause
# Wait for the deployment to complete
$ watch -n1 --color "juju status --color"
```
