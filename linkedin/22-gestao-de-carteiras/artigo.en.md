# Member portfolio management

*Services on EKS, notifications on Lambda and private integration with the data lake.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Member portfolio management](https://raphaelfcs.github.io/portfolio/artigos/img/gestao-de-carteiras-en-1.webp)

> **TL;DR:** EKS and Lambda in the same product: each where it makes sense.

## Problem

Member portfolio management with continuous parts and event-driven parts.

## Solution

Core API on EKS, notifications on Lambda, database backup with a dedicated plan and private integration with the data lake account.

### Member portfolio management

1. Portal and app through CloudFront.
2. APIs on API Gateway.
3. Link and classification services on EKS.
4. Data in RDS with backup.
5. Lambda sends notifications.
6. Integration with the data lake over private network.

## The code

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "vpc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/vpc"

  name_prefix        = local.name_prefix
  cidr_block         = "10.20.0.0/16"
  azs                = ["sa-east-1a", "sa-east-1b"]
  single_nat_gateway = true
  eks_cluster_name   = "demo-dev"
  tags               = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/gestao-de-carteiras/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
