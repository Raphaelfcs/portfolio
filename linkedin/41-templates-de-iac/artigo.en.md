# Developer portal with IaC templates

*Backstage, tenant/domain/system templates, PR, approval and in-account apply, with an RDS example.*

Raphael Santos · 3 min read · Developer portal and infrastructure templates (2024)

![Developer portal with IaC templates](https://raphaelfcs.github.io/portfolio/artigos/img/templates-de-iac-en-1.webp)

> **TL;DR:** Developer portal with IaC templates: from MVP to full architecture.

## Problem

Teams requesting infrastructure through tickets and waiting days.

## Solution

Backstage templates per tenant, domain and system, a generated PR, checks, approval and apply with an assumed role in the target account, with a full RDS example.

### Developer portal with IaC templates

1. Developer opens the portal.
2. Picks a template and fills a few fields.
3. Portal generates code and opens a PR.
4. PR runs checks; merging into main triggers deployment.
5. Apply only after approval, with an assumed role.
6. Resource shows up in the catalog.

### Example: RDS through the portal (MVP)

1. First template creates the instance.
2. In-VPC runner applies Terraform.
3. Second template creates the database on the instance.
4. Credential goes to Secrets Manager.

![Figure 2: Example: RDS through the portal (MVP)](https://raphaelfcs.github.io/portfolio/artigos/img/templates-de-iac-en-2.webp)
*Figure 2: Example: RDS through the portal (MVP)*

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

**Terraform modules used:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/templates-de-iac/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
