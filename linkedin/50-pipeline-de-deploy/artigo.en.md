# Deployment pipeline per environment

*Image built once from a template and promoted from DEV to PRD.*

Raphael Santos · 3 min read · Benefits platform on AWS (2023)

![Deployment pipeline per environment](https://raphaelfcs.github.io/portfolio/artigos/img/pipeline-de-deploy-en-1.webp)

> **TL;DR:** A per-environment pipeline starts with the image template.

## Problem

Manual deploys and different images in each environment.

## Solution

Image built once from a template, pushed to the registry and promoted to DEV, QA and PRD with approval.

### Deployment pipeline per environment

1. Template standardizes the image.
2. Pipeline pushes to ECR.
3. Deploy to DEV.
4. Same image promoted to QA.
5. PRD with approval.

## The code

```hcl
module "iam_github_oidc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-github-oidc"

  github_org           = "minha-org"
  github_repo          = "infra"
  allowed_environments = ["dev", "prd"]
  managed_role_prefix  = "app-"
  state_bucket_arn     = "arn:aws:s3:::demo-tfstate-123456789012"
  tags                 = local.tags
}

module "ecr" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/ecr"

  name_prefix      = "demo"
  repository_names = ["api", "worker"]
  tags             = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/ecr | old images piling up in ECR | lifecycle policy keeping only the last N images per repository |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/beneficios/pipeline-de-deploy/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
