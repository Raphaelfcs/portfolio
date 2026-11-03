# External Kong in the GKE DMZ

*Cloud Armor, external LB, network-policy-isolated Kong and an internal LB to the microservices.*

Raphael Santos · 3 min read · Network, gateways and data on Google Cloud (2024)

![External Kong in the GKE DMZ: AS-IS vs TO-BE](https://raphaelfcs.github.io/portfolio/artigos/img/api-gateway-externo-kong-en-1.webp)

> **TL;DR:** Kong in the GKE DMZ: AS-IS vs TO-BE.

## Problem

External gateway exposed without clear separation between environments.

## Solution

Cloud Armor and an external LB that only reaches Kong on port 8000, Kong isolated with a deny-all network policy and an internal LB to the microservices per environment.

### External Kong in the GKE DMZ: AS-IS vs TO-BE

1. Edge with Cloud Armor.
2. External LB only reaches Kong on port 8000.
3. Kong calls the internal LB.
4. Microservices isolated per environment.

> **Note:** Kong namespace with deny-all ingress and egress, allowing only what is needed.

## The code

```hcl
module "project_foundation" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//gcp/project-foundation"

  project_id       = "demo-plataforma-dev"
  project_name     = "Demo Plataforma"
  billing_account  = "000000-000000-000000"
  apis             = ["compute.googleapis.com", "container.googleapis.com", "sqladmin.googleapis.com"]
  boolean_policies = ["compute.skipDefaultNetworkCreation", "iam.disableServiceAccountKeyCreation", "storage.uniformBucketLevelAccess"]
  labels           = local.labels
}

module "vpc_network" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//gcp/vpc-network"

  project_id = module.project_foundation.project_id
  region     = local.region
  subnet     = { name = "sn-gke-sp", cidr = "10.10.0.0/20", pods_cidr = "10.20.0.0/16", services_cidr = "10.30.0.0/20" }
  psa_range  = { address = "10.40.0.0", prefix_length = 16 }
}
```

## Discussion

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/gke-private](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/gke-private), [gcp/edge-load-balancer](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/edge-load-balancer)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/gke-private | GKE nodes (or pods on Autopilot) | Autopilot to pay per pod, Spot VMs and CUDs for the baseline |
| gcp/vpc-network | Cloud NAT and cross-zone/region traffic | Private Google Access and keep traffic in the same region |
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |
| gcp/edge-load-balancer | forwarding rules and Cloud Armor | consolidate rules and use Cloud CDN for caching |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/consultoria-gcp/api-gateway-externo-kong/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
