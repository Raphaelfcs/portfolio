# Template workflow: multi-repo vs monorepo

*Application and infra repositories, CI/CD and Atlantis, compared with a monorepo.*

Raphael Santos · 3 min read · Developer portal and infrastructure templates (2024)

![Template workflow: multi-repo vs monorepo](https://raphaelfcs.github.io/portfolio/artigos/img/workflow-multi-x-mono-repo-en-1.webp)

> **TL;DR:** IaC templates: multi-repo or monorepo?

## Problem

Template platform needing to decide how to organize repositories.

## Solution

Application and infra repositories with CI/CD and Atlantis, compared side by side with the monorepo option.

### Template workflow: multi-repo vs monorepo

1. Developer picks the template.
2. Portal creates the repositories.
3. CI builds and pushes the image.
4. CD deploys to ECS.
5. Separate infra, applied by Atlantis.

> **Note:** In the monorepo, app and terraform/ live in one repository with separate pipelines.

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

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/workflow-multi-x-mono-repo/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
