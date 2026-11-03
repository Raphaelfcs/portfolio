# Medical equipment reimbursement API

*BFF on ECS Fargate, serverless MySQL and FIFO queue integrations with DLQ.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Medical equipment reimbursement API](https://raphaelfcs.github.io/portfolio/artigos/img/api-equipamentos-medicos-en-1.webp)

> **TL;DR:** A BFF on ECS with a pipeline: simple, cheap and easy to operate.

## Problem

Medical equipment reimbursement API consumed by a portal and partners.

## Solution

BFF on ECS Fargate behind API Gateway and WAF, serverless MySQL, FIFO queue integrations with DLQ and a pipeline from day one.

### Medical equipment reimbursement API

1. WAF-protected entry.
2. API Gateway to the BFF on Fargate.
3. Data in serverless MySQL.
4. Asynchronous integrations through a FIFO queue.
5. Internal services consume the queue.
6. Pipeline pushes the image and deploys.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/ecr | old images piling up in ECR | lifecycle policy keeping only the last N images per repository |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/api-equipamentos-medicos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
