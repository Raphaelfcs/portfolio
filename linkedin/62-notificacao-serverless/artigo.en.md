# Two-AZ application with notifications

*IaC assignment: ELB, web servers in two AZs, RDS and SNS through a private endpoint.*

Raphael Santos · 3 min read · Architecture technical challenges

![Two-AZ application with notifications](https://raphaelfcs.github.io/portfolio/artigos/img/notificacao-serverless-en-1.webp)

> **TL;DR:** Two-AZ application with notifications: a postgraduate IaC assignment.

## Problem

IaC exercise requiring high availability and event notifications.

## Solution

Two zones, a load balancer, a managed database and SNS through a private endpoint, all described in code.

### Two-AZ application with notifications

1. User access.
2. ELB spreads across two AZs.
3. Database write.
4. Notification through the private SNS endpoint.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |
| aws/sns-topic | messages and deliveries per protocol | subscription filters so consumers do not receive what they discard |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/desafios/notificacao-serverless/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
