# Architecture evolution in three horizons

*Three-horizon modernization roadmap (stabilize, integrate, innovate) for a mid-size company with legacy systems.*

Raphael Santos · 3 min read · Architecture case studies (2026)

![Case 1 — Evolution architecture (H1, H2, H3)](https://raphaelfcs.github.io/portfolio/artigos/img/transformacao-digital-h1-h3-en-1.webp)

> **TL;DR:** Modernizing everything at once usually fails. I prefer three horizons.

## Problem

Mid-size company with legacy systems, little automation and a small infrastructure team.

## Solution

H1 stabilizes (accounts, guardrails, backup), H2 integrates (network, containers, data) and H3 innovates. Each horizon delivers value on its own, and the next one only starts when the previous one is stable.

## The code

```hcl
module "organizations_scp" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/organizations-scp"

  allowed_regions        = ["sa-east-1", "us-east-1"]
  required_tags          = ["CentroCusto", "Ambiente", "Dono"]
  create_tag_enforcement = ["CentroCusto"]
  attach_target          = ["Workloads", "Sandbox"]
  tags                   = local.tags
}

module "security_baseline" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/security-baseline"

  tags = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/backup-plan | recovery point retention | retention by criticality and cold storage for long-term copies |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/estudos-de-caso/transformacao-digital-h1-h3/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
