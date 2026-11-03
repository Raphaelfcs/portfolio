# AI process automation MVP

*MVP that receives documents, extracts data with managed AI and returns the result to the source system with full traceability.*

Raphael Santos · 3 min read · Architecture case studies (2026)

![Case 2 — MVP architecture](https://raphaelfcs.github.io/portfolio/artigos/img/automacao-com-ia-mvp-en-1.webp)

> **TL;DR:** An AI MVP does not need a GPU cluster. It needs traceability.

## Problem

Manual document-reading process, with rework and no trail of who did what.

## Solution

Textract + queues + an event bus solve 80% of the problem with managed services; what makes the MVP trustworthy is that every document has a state, an owner and a history.

## The code

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "textract_pipeline" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/textract-pipeline"

  name_prefix = "demo-dev-ocr"
  kms_key_arn = module.kms_key.key_arn
  tags        = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/textract-pipeline | Textract cost per processed page | filter and classify before extracting and use only the needed features (text vs forms vs tables) |
| aws/cloudfront-spa | CDN data transfer | good caching and compression; the CDN usually lowers origin egress cost |
| aws/cognito-user-pool | Cognito monthly active users (MAU) | pick the right tier and clean up inactive accounts |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/estudos-de-caso/automacao-com-ia-mvp/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
