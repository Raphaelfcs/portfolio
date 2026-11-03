# Guardrails for S3, RDS and CloudFront

*Preventive controls via SCP and boundaries, detective via Config and lifecycle via IaC.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Guardrails for S3, RDS and CloudFront](https://raphaelfcs.github.io/portfolio/artigos/img/guardrails-s3-rds-cloudfront-en-1.webp)

> **TL;DR:** A good guardrail stops the mistake before the deploy.

## Problem

Public buckets by accident, unencrypted databases and distributions without minimum TLS.

## Solution

Preventive controls with SCP and permission boundaries, detective controls with Config and GuardDuty, and lifecycle to Glacier through IaC.

### Guardrails for S3, RDS and CloudFront

1. SCPs applied at the organization.
2. Buckets with no public access and encryption.
3. Lifecycle to Glacier via IaC.
4. Multi-AZ RDS, no deletion outside the process.
5. Config detects non-compliant distributions.

> **Note:** References: LGPD, ISO 27001 and ISO 27005.

## The code

```hcl
module "organizations_scp" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/organizations-scp"

  allowed_regions        = ["sa-east-1", "us-east-1"]
  required_tags          = ["CentroCusto", "Ambiente", "Dono"]
  create_tag_enforcement = ["CentroCusto"]
  attach_target          = ["Workloads", "Sandbox"]
  tags                   = local.tags
}

module "security_baseline" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/security-baseline"

  tags = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/rds-instance | RDS instance class and Multi-AZ | right-size from real metrics, reserve PRD and stop HML/DEV after hours |
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |
| aws/security-baseline | Config, GuardDuty and Security Hub in every account | record only the relevant resource types in Config |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/guardrails-s3-rds-cloudfront/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
