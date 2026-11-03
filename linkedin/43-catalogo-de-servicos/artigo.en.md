# Self-service catalog

*From a Backstage request to a resource in the account, with the credential in Secrets Manager.*

Raphael Santos · 3 min read · Developer portal and infrastructure templates (2024)

![Self-service catalog](https://raphaelfcs.github.io/portfolio/artigos/img/catalogo-de-servicos-en-1.webp)

> **TL;DR:** Infrastructure self-service starts in the catalog.

## Problem

Developers with no standard path to request resources.

## Solution

From the catalog to provisioning: the developer picks, the portal writes code to Git, the pipeline applies and the credential lands in Secrets Manager.

### Self-service catalog

1. Developer requests from the catalog.
2. Portal writes code to Git.
3. Pipeline applies.
4. Database created in the account.
5. Credential in Secrets Manager.

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

**Terraform modules used:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/catalogo-de-servicos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
