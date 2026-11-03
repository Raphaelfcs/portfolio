# Secure GKE end to end

*Private GKE lab with Workload Identity, private Cloud SQL, Pub/Sub and a Cloud Armor edge.*

Raphael Santos · 3 min read · Google Cloud reference architectures (2026)

![1 · Architecture and journey](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-en-1.webp)

> **TL;DR:** "Secure" GKE is a list of decisions, not a console checkbox.

## Problem

Lab to show private GKE end to end, from the edge to the database.

## Solution

Private cluster, Workload Identity (no service account keys), Cloud SQL on private IP only, Cloud Armor at the edge and Pub/Sub to decouple. The numbered journey in the drawing is the same one the code implements.

![Figure 2: 2 · Foundation and IAM](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-en-2.webp)
*Figure 2: 2 · Foundation and IAM*

![Figure 3: 3 · Terraform structure](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-en-3.webp)
*Figure 3: 3 · Terraform structure*

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

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/gke-private](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/gke-private), [gcp/cloud-sql](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/cloud-sql), [gcp/pubsub](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/pubsub), [gcp/edge-load-balancer](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/edge-load-balancer)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/gke-private | GKE nodes (or pods on Autopilot) | Autopilot to pay per pod, Spot VMs and CUDs for the baseline |
| gcp/cloud-sql | Cloud SQL vCPU/memory and HA | right-size from metrics, CUDs for PRD and stop non-production |
| gcp/vpc-network | Cloud NAT and cross-zone/region traffic | Private Google Access and keep traffic in the same region |
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/google-cloud/gke-seguro/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
