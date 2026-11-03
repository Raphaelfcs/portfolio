# Shared EKS cluster

*Multi-tenant cluster with a namespace per app, HPA, quotas and shared services.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Shared platform EKS cluster](https://raphaelfcs.github.io/portfolio/artigos/img/cluster-eks-en-1.webp)

> **TL;DR:** A shared EKS cluster needs clear rules before the first deploy.

## Problem

Several applications moving into the same EKS cluster.

## Solution

Namespace per application with HPA, limits and quotas, internal NLB behind API Gateway, images only from the shared ECR and a queue and database per app.

### Shared platform EKS cluster

1. Edge with CloudFront and WAF.
2. API Gateway publishes routes.
3. VPC link to the internal NLB.
4. Ingress routes per namespace (multi-tenant).
5. Each app uses its own queue and database.

> **Note:** Namespace per app with HPA, limits and quotas; label affinity separates tenants.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/ecr | old images piling up in ECR | lifecycle policy keeping only the last N images per repository |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/cluster-eks/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
