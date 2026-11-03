# Partner network integration

*Transit Gateway peering for Diameter signaling and data in private subnets.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![Partner network integration via Transit Gateway](https://raphaelfcs.github.io/portfolio/artigos/img/integracao-rede-parceiro-en-1.webp)

> **TL;DR:** Integrating a partner network without mixing responsibilities.

## Problem

Platform needing to exchange Diameter signaling with a partner network.

## Solution

Transit Gateway peering as the single point, SCTP to the gateway on EKS, private DNS between sides and data services in private subnets only. All measured in the account, not inferred.

### Partner network integration via Transit Gateway

1. Signaling peers enter through the partner network.
2. Transit Gateway peering.
3. SCTP traffic reaches the gateway on EKS.
4. Data only in private subnets.

> **Note:** Measured in the account (read-only scan), not inferred from code.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/route53-private-zone](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-private-zone), [aws/msk-kafka](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/msk-kafka), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/msk-kafka | MSK brokers and storage | per-topic retention, tiered storage and Graviton brokers |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/transit-gateway-attachment | Transit Gateway attachments and processed GB | consolidate attachments and keep high-volume traffic off the TGW |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/integracao-rede-parceiro/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
