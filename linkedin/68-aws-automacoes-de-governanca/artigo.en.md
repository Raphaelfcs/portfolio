# Event-driven governance automations on AWS

*Tags, MFA, IAM inventory, certificates, security findings and cost: what I automate with CloudTrail, EventBridge and Lambda.*

Raphael Santos · 4 min read · Hands-on AWS

![aws/tag-compliance: Event-driven tag compliance](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-en-1.webp)

> **TL;DR:** Governance that depends on someone remembering to look at a screen does not happen. It has to react to the event the moment it happens.

## Problem

I started in 2017 with boto3 scripts on cron: EC2 autotagging, stopping untagged RDS, checking MFA, listing expiring certificates. They worked, but they had fixed credentials, email recipients hardcoded and no logs with retention.

## Solution

I redesigned each automation as an event-driven Terraform module. A resource creation recorded in CloudTrail reaches EventBridge and triggers the tag compliance Lambda. A managed Config rule checks MFA continuously, and a weekly Lambda sends the report. The IAM inventory is exported weekly as versioned JSON in S3. Certificates alert through ACM’s native event, with no code. GuardDuty and Security Hub findings reach SNS through EventBridge. EC2 and RDS start and stop by tag with EventBridge Scheduler, and a daily cost report comes out of Cost Explorer.

### What each automation does

1. tag-compliance: CloudTrail → EventBridge → Lambda applies and validates tags on create and alerts through SNS.
2. iam-mfa-audit: a continuous Config rule and a weekly Lambda listing console users without MFA.
3. iam-inventory-export: users, groups, roles and policies as JSON in a versioned, encrypted S3 bucket.
4. acm-expiry-alert: ACM’s own expiration event becomes an alert, with no Lambda scanning certificates.
5. security-baseline: GuardDuty, Security Hub, Inspector and Macie findings through EventBridge → SNS.
6. instance-scheduler and finops-cost-report: start/stop by tag with time zones, and the day’s cost on SNS.

> **Note:** Each Lambda has its own least-privilege role, a log group with retention and KMS, and an error alarm. No fixed credentials.

![Figure 2: aws/iam-mfa-audit: MFA audit](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-en-2.webp)
*Figure 2: aws/iam-mfa-audit: MFA audit*

![Figure 3: aws/instance-scheduler: FinOps scheduler for EC2/RDS](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-en-3.webp)
*Figure 3: aws/instance-scheduler: FinOps scheduler for EC2/RDS*

## The code

```hcl
module "tag_compliance" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tag-compliance?ref=main"

  name_prefix     = local.name_prefix
  required_tags   = ["CentroCusto", "Ambiente", "Dono"]
  alert_topic_arn = "arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"
  tags            = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/tag-compliance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tag-compliance), [aws/iam-mfa-audit](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-mfa-audit), [aws/iam-inventory-export](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-inventory-export), [aws/acm-expiry-alert](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/acm-expiry-alert), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/instance-scheduler](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/instance-scheduler), [aws/finops-cost-report](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/finops-cost-report)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/instance-scheduler | Dev and staging environments running at night and on weekends. | Stop by tag on a business-hours schedule. |
| aws/tag-compliance | Cost with no owner, which nobody can cut. | Mandatory tags applied on create, not at the monthly review. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/tag-compliance/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
