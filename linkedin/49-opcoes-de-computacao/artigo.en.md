# Compute options: ECS, EKS and Beanstalk

*The same benefits app drawn on all three options, sharing edge and database.*

Raphael Santos · 3 min read · Benefits platform on AWS (2023)

![Same application on ECS Fargate](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-en-1.webp)

> **TL;DR:** ECS Fargate, EKS or Beanstalk? I drew all three for the same app.

## Problem

Benefits platform leaving traditional servers.

## Solution

Three drawings sharing the edge (CDN/WAF), registry and database. The comparison stayed fair and the decision documented.

### Same application on ECS Fargate

1. Edge with CloudFront and WAF.
2. ALB spreads across tasks.
3. Private database and cache.

### Same application on EKS

1. Same edge.
2. Ingress splits API and web by namespace.
3. Same private data.

### Same application on Elastic Beanstalk

1. Same edge.
2. Reads and writes split.
3. Jobs isolated to scale out.

> **Note:** All three versions share edge, registry and database: a fair comparison.

![Figure 2: Same application on EKS](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-en-2.webp)
*Figure 2: Same application on EKS*

![Figure 3: Same application on Elastic Beanstalk](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-en-3.webp)
*Figure 3: Same application on Elastic Beanstalk*

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/elasticache-redis | ElastiCache nodes running 24/7 | smaller Graviton node type and reservation for PRD |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/beneficios/opcoes-de-computacao/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
