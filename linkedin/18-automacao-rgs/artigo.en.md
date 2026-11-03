# Operational routine automation with AI

*S3 event triggers Lambda, Textract, Rekognition and Comprehend; result in DynamoDB with an API.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Operational routine automation with AI](https://raphaelfcs.github.io/portfolio/artigos/img/automacao-rgs-en-1.webp)

> **TL;DR:** A manual operational routine is a natural candidate for event-driven AI.

## Problem

Daily routine done by hand, with spreadsheets and visual checks.

## Solution

An S3 event triggers Lambda, which calls Textract, Rekognition and Comprehend; the result lands in DynamoDB behind an API. The routine now has logs and failure alerts.

### Operational routine automation with AI

1. File lands in S3.
2. Event triggers Lambda.
3. Textract extracts text; Rekognition analyzes images.
4. Comprehend classifies the content.
5. Result stored in DynamoDB.
6. Queried through an API.

## The code

```hcl
module "s3_bucket" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/s3-bucket"

  bucket_name = "demo-dev-dados-123456789012"
  tags        = local.tags
}

module "lambda_function" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/lambda-function"

  function_name       = "demo-dev-relatorio"
  source_dir          = "${path.module}/src"
  schedule_expression = "rate(1 day)"
  environment         = { NIVEL_LOG = "INFO" }
  tags                = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/textract-pipeline | Textract cost per processed page | filter and classify before extracting and use only the needed features (text vs forms vs tables) |
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/automacao-rgs/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
