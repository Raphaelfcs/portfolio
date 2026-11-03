# Cloud SQL data lifecycle

*Split reads and writes, age-based purge to Cloud Storage and historical queries in BigQuery.*

Raphael Santos · 3 min read · Network, gateways and data on Google Cloud (2024)

![Cloud SQL data lifecycle](https://raphaelfcs.github.io/portfolio/artigos/img/ciclo-de-vida-cloud-sql-en-1.webp)

> **TL;DR:** A transactional database is no place for data from 10 years ago.

## Problem

Cloud SQL growing endlessly with rarely queried historical data.

## Solution

Current year in Cloud SQL with split reads and writes, yearly purge to Cloud Storage with age-based classes and historical queries in BigQuery.

### Cloud SQL data lifecycle

1. Writes go to the primary.
2. Reads go to the replica with the current year.
3. Yearly purge to Cloud Storage.
4. Storage classes by age.
5. BigQuery queries history without touching the database.

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

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/cloud-sql](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/cloud-sql)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/cloud-sql | Cloud SQL vCPU/memory and HA | right-size from metrics, CUDs for PRD and stop non-production |
| gcp/vpc-network | Cloud NAT and cross-zone/region traffic | Private Google Access and keep traffic in the same region |
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/consultoria-gcp/ciclo-de-vida-cloud-sql/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
