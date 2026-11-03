# FinOps process

*Inform, optimize and operate cycle, with owners, cadence and guardrails.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![FinOps process: inform, optimize, operate](https://raphaelfcs.github.io/portfolio/artigos/img/processo-finops-en-1.webp)

> **TL;DR:** FinOps is a cycle: inform, optimize and operate, every week.

## Problem

Cloud bill growing with no clear owner for each cost.

## Solution

Mandatory tags and CUR/FOCUS exports feed the report, KPIs per area drive recommendations, a mixed team executes and what repeats becomes a guardrail or an automated schedule.

### FinOps process: inform, optimize, operate

1. Mandatory tags and cost exports feed the report.
2. KPIs per area and showback/chargeback.
3. Deviations become prioritized recommendations.
4. Mixed team executes with resource owners.
5. What repeats becomes a guardrail or an automated schedule.

## The code

```hcl
module "cur_focus_export" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/cur-focus-export"

  bucket_name    = "demo-finops-focus-123456789012"
  retention_days = 730
  tags           = local.tags
}

module "finops_cost_report" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/finops-cost-report"

  name_prefix         = local.name_prefix
  bucket_name         = "demo-finops-relatorios-123456789012"
  alert_topic_arn     = "arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"
  cost_allocation_tag = "CentroCusto"
  tags                = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/cur-focus-export](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cur-focus-export), [aws/finops-cost-report](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/finops-cost-report), [aws/tag-compliance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tag-compliance), [aws/instance-scheduler](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/instance-scheduler)

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
