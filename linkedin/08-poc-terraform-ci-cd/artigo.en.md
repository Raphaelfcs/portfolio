# Terraform CI/CD POC on Google Cloud

*GitHub Actions with Workload Identity Federation, one service account per environment and remote state.*

Raphael Santos · 3 min read · Google Cloud reference architectures (2026)

![Terraform CI/CD POC on Google Cloud](https://raphaelfcs.github.io/portfolio/artigos/img/poc-terraform-ci-cd-en-1.webp)

> **TL;DR:** Terraform CI/CD POC on Google Cloud.

## Problem

Proof of concept to validate an IaC pipeline before adopting it in production.

## Solution

GitHub Actions with Workload Identity Federation (no JSON keys), one service account per environment, remote state and the public site closed at night.

### Terraform CI/CD POC on Google Cloud

1. Mandatory PR, no direct push.
2. CI runs lint, tests and plan.
3. No JSON key: GitHub OIDC.
4. One service account per environment.
5. Apply and smoke test; public access closed at night.

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

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/vpc-network | Cloud NAT and cross-zone/region traffic | Private Google Access and keep traffic in the same region |
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/google-cloud/poc-terraform-ci-cd/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
