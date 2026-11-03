# Debt negotiation portal

*The same app drawn on EKS and on ECS to decide based on operations and cost.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Debt negotiation portal — EKS](https://raphaelfcs.github.io/portfolio/artigos/img/negociacao-de-debitos-en-1.webp)

> **TL;DR:** I drew the same application on EKS and on ECS to decide with numbers.

## Problem

Debt negotiation portal with doubts between EKS and ECS.

## Solution

Two versions of the drawing, same edge, same database, same pipeline. The decision came from operations and cost, not preference.

### Debt negotiation portal — EKS

1. WAF edge.
2. Static front-end.
3. API Gateway to the BFF.
4. BFF calls the business API.
5. Data in serverless MySQL.
6. Integrations through a FIFO queue.

### Debt negotiation portal — ECS

1. API Gateway at the entry.
2. ALB spreads across tasks.
3. Same database as the EKS design.
4. Same queue integrations.
5. Same pipeline: image + tag on ECR.

![Figure 2: Debt negotiation portal — ECS](https://raphaelfcs.github.io/portfolio/artigos/img/negociacao-de-debitos-en-2.webp)
*Figure 2: Debt negotiation portal — ECS*

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/cloudfront-spa | CDN data transfer | good caching and compression; the CDN usually lowers origin egress cost |
| aws/ecr | old images piling up in ECR | lifecycle policy keeping only the last N images per repository |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/negociacao-de-debitos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
