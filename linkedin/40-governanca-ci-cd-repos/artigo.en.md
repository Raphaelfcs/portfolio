# CI/CD governance for Terraform repositories

*Boilerplate, CCoE-reviewed merge requests and apply with federated identity.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![CI/CD governance for Terraform repositories](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-ci-cd-repos-en-1.webp)

> **TL;DR:** CI/CD governance for Terraform repositories.

## Problem

Several teams applying Terraform with no approval standard.

## Solution

Boilerplate, workload repository, merge request reviewed by the CCoE and apply with federated identity instead of keys.

### CI/CD governance for Terraform repositories

1. Team starts from the boilerplate.
2. Creates the workload repository.
3. Merge request reviewed by the CCoE.
4. Once approved, the pipeline runs.
5. Applies to accounts with federated identity.

## The code

```hcl
module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}

module "iam_github_oidc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-github-oidc"

  github_org           = "minha-org"
  github_repo          = "infra"
  allowed_environments = ["dev", "prd"]
  managed_role_prefix  = "app-"
  state_bucket_arn     = "arn:aws:s3:::demo-tfstate-123456789012"
  tags                 = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | resources without an owner and non-production environments running 24/7 | mandatory tags and after-hours shutdown |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/governanca-ci-cd-repos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
