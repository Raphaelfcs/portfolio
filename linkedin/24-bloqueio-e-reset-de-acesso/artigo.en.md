# Shared access lock and reset

*EKS service consumed by AWS and OCI systems through Transit Gateway and VPN.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Shared access lock and reset](https://raphaelfcs.github.io/portfolio/artigos/img/bloqueio-e-reset-de-acesso-en-1.webp)

> **TL;DR:** A service shared between AWS and OCI: the network is half the project.

## Problem

Credential lock and reset used by several systems, some outside AWS.

## Solution

Service on EKS behind API Gateway and WAF, egress through the network account Transit Gateway and site-to-site VPN to OCI.

### Shared access lock and reset

1. Portals call the service through the edge.
2. API Gateway to EKS.
3. Egress via the network account Transit Gateway.
4. VPN to the OCI systems.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/vpn-site-to-site](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpn-site-to-site)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eks-cluster | EKS nodes (EC2) and the per-cluster control plane | node autoscaling (Karpenter/Cluster Autoscaler), Spot for tolerant workloads and Savings Plans for the baseline |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/transit-gateway-attachment | Transit Gateway attachments and processed GB | consolidate attachments and keep high-volume traffic off the TGW |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/bloqueio-e-reset-de-acesso/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
