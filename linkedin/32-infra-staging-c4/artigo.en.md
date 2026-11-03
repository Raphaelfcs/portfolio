# Staging infrastructure in C4

*C4 context of the platform and the IaC permission model with four separate identities.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![Staging infrastructure — context (C4 level 1)](https://raphaelfcs.github.io/portfolio/artigos/img/infra-staging-c4-en-1.webp)

> **TL;DR:** C4 Model for infrastructure: it works, and very well.

## Problem

Staging environment with several stacks and unclear permissions.

## Solution

A C4 context of the platform and a permission model with four identities that never overlap: the operator applies infra, CI only pushes images, ArgoCD pulls from git and pods read only their secret prefix.

### Staging infrastructure — context (C4 level 1)

1. Access through CDN and ALB.
2. Workloads on the workload cluster.
3. Events published to managed Kafka.
4. Pinot serves real-time queries.
5. Transactional data and cache in private subnets.
6. Operator systems arrive through Transit Gateway.

### IaC permissions: four identities that never overlap

1. Only the operator applies infra, after reviewing the plan.
2. CI pushes images and nothing else.
3. ArgoCD pulls state from git (pull-based).
4. Pods read only their secret prefix.

![Figure 2: IaC permissions: four identities that never overlap](https://raphaelfcs.github.io/portfolio/artigos/img/infra-staging-c4-en-2.webp)
*Figure 2: IaC permissions: four identities that never overlap*

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

**Terraform modules used:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/elasticache-redis | ElastiCache nodes running 24/7 | smaller Graviton node type and reservation for PRD |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/infra-staging-c4/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
