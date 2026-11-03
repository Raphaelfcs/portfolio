# Multicloud charging platform

*The platform today on AWS and the equivalence map to Google Cloud, Azure and on-premises.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![Charging platform — AWS today](https://raphaelfcs.github.io/portfolio/artigos/img/plataforma-multicloud-en-1.webp)

> **TL;DR:** The same platform on AWS, GCP, Azure and on-premises.

## Problem

Charging platform that had to be portable across clouds.

## Solution

The AWS design as it runs today and an equivalence map per function. It helped separate what belongs to the application from what belongs to the provider.

### Charging platform — AWS today

1. CI pushes images through OIDC.
2. ArgoCD hub syncs the clusters.
3. Peers arrive through Transit Gateway.
4. Workload publishes events and uses database and cache.
5. Operations only through SSM, no SSH.

![Figure 2: Cross-cloud equivalence map](https://raphaelfcs.github.io/portfolio/artigos/img/plataforma-multicloud-en-2.webp)
*Figure 2: Cross-cloud equivalence map*

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/msk-kafka](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/msk-kafka), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/msk-kafka | MSK brokers and storage | per-topic retention, tiered storage and Graviton brokers |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/plataforma-multicloud/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
