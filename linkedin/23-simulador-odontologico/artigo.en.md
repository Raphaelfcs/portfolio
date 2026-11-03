# Cost preview simulator

*Static front-end with WAF and calculation on EKS.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Cost preview simulator](https://raphaelfcs.github.io/portfolio/artigos/img/simulador-odontologico-en-1.webp)

> **TL;DR:** A simple simulator still deserves proper architecture.

## Problem

Cost preview simulator used by customers on the portal.

## Solution

Static front-end on the CDN behind WAF, calculation API on EKS. Few components, few things to break.

### Cost preview simulator

1. User resolves the domain.
2. WAF security layer.
3. Front-end served from S3.
4. Calculation calls go to the API.
5. Calculation runs on EKS.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa), [aws/route53-private-zone](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-private-zone)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/cloudfront-spa | CDN data transfer | good caching and compression; the CDN usually lowers origin egress cost |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/simulador-odontologico/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
