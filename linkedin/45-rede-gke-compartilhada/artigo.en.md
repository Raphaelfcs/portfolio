# Shared VPC for GKE and databases

*Network host project, service projects, service peering and VPN per environment.*

Raphael Santos · 3 min read · Network, gateways and data on Google Cloud (2024)

![Shared VPC for GKE and databases](https://raphaelfcs.github.io/portfolio/artigos/img/rede-gke-compartilhada-en-1.webp)

> **TL;DR:** Shared VPC with GKE and managed databases: watch the peerings.

## Problem

Service projects with GKE needing to reach databases in other projects.

## Solution

Central host project, service projects, service peering for databases and VPN per environment, with ranges planned up front.

### Shared VPC for GKE and databases

1. Pipeline deploys to GKE.
2. Services exposed through an internal LB.
3. Cluster uses host project subnets.
4. Databases via service peering.
5. Peerings and VPN per environment with planned ranges.

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

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/gke-private](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/gke-private), [gcp/cloud-sql](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/cloud-sql)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/gke-private | GKE nodes (or pods on Autopilot) | Autopilot to pay per pod, Spot VMs and CUDs for the baseline |
| gcp/cloud-sql | Cloud SQL vCPU/memory and HA | right-size from metrics, CUDs for PRD and stop non-production |
| gcp/vpc-network | Cloud NAT and cross-zone/region traffic | Private Google Access and keep traffic in the same region |
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/consultoria-gcp/rede-gke-compartilhada/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
