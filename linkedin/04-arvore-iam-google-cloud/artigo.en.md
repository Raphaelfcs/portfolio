# Google Cloud resource and permission tree

*Organization, per-environment folders, projects and groups with roles granted at the right level of the hierarchy.*

Raphael Santos · 3 min read · Architecture case studies (2026)

![Google Cloud — resource and permission tree](https://raphaelfcs.github.io/portfolio/artigos/img/arvore-iam-google-cloud-en-1.webp)

> **TL;DR:** A permission at the wrong level of the hierarchy becomes security debt.

## Problem

Teams needing project access without anyone becoming Owner of the organization.

## Solution

Roles granted to groups at the right level (organization, folder or project) and never to users. The resource tree is the IAM design.

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
```

## Discussion

**Terraform modules used:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| gcp/project-foundation | cost starts in projects without an owner | labels on every project (the module already applies them) and a budget alert in Billing |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/estudos-de-caso/arvore-iam-google-cloud/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
