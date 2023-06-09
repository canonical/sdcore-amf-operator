<div align="center">
  <img src="./icon.svg" alt="ONF Icon" width="200" height="200">
</div>
<div align="center">
  <h1>SD-Core AMF Operator</h1>
</div>

# sdcore-amf-operator

Charmed Operator for SD-Core's Access and Mobility Management Function (AMF).


## Pre-requisites

Juju model on a Kubernetes cluster.

## Usage

```bash
juju deploy sdcore-amf --trust --channel=edge
juju deploy mongodb-k8s --trust --channel=5/edge
juju deploy sdcore-nrf --trust --channel=edge
juju integrate sdcore-amf:default-database mongodb-k8s
juju integrate sdcore-amf:amf-database mongodb-k8s
juju integrate sdcore-amf:fiveg-nrf sdcore-nrf:fiveg-nrf
```

### Optional

```bash
juju deploy self-signed-certificates --channel=edge
juju integrate sdcore-amf:certificates self-signed-certificates:certificates
```

## Image

**amf**: ghcr.io/canonical/sdcore-amf:1.3
