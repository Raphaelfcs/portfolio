# AWS platform of a health insurer

*Multi-region backup over a shared network and the IaC evolution to one state per resource and environment.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Multi-region backup with shared network](https://raphaelfcs.github.io/portfolio/artigos/img/visao-geral-plataforma-en-1.webp)

> **TL;DR:** Backing up 230 TB a month across regions without touching the internet.

## Problem

Large AWS platform at a health insurer, with workloads in two regions and backup handled by agents next to the applications.

## Solution

Separate accounts for application, network and backup, traffic through the shared Transit Gateway, S3 through VPC endpoints and lifecycle to Glacier. On the IaC side, we moved from one state for everything to one state per resource and environment.

### Multi-region backup with shared network

1. Backup agents run next to workloads, in Auto Scaling.
2. Backup traffic goes through the network account Transit Gateway (TCP 8400-8410).
3. Active orchestrator in us-east-1, passive in sa-east-1.
4. Writes to S3 IA through a VPC endpoint, no internet.
5. Lifecycle moves old copies to Glacier Deep Archive.
6. Cross-region replica for DR.

> **Note:** Separate application, network and backup accounts reduce blast radius.

### IaC: one state per resource and environment

1. v0: one state for everything; any change risked the whole platform.
2. v1: pipeline per resource and environment.
3. Each resource has its own backend and lifecycle.
4. Dependencies through outputs and depends_on, never hard-coded IDs.

![Figure 2: IaC: one state per resource and environment](https://raphaelfcs.github.io/portfolio/artigos/img/visao-geral-plataforma-en-2.webp)
*Figure 2: IaC: one state per resource and environment*

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/vpc-endpoints](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc-endpoints), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/transit-gateway-attachment | Transit Gateway attachments and processed GB | consolidate attachments and keep high-volume traffic off the TGW |
| aws/ecr | old images piling up in ECR | lifecycle policy keeping only the last N images per repository |
| aws/backup-plan | recovery point retention | retention by criticality and cold storage for long-term copies |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/visao-geral-plataforma/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
