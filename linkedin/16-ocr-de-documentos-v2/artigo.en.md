# Document OCR — API v2

*Serverless back-office with an authorizer and one function per resource.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Document OCR — asynchronous API v2](https://raphaelfcs.github.io/portfolio/artigos/img/ocr-de-documentos-v2-en-1.webp)

> **TL;DR:** Version 2 of an API is usually about what went wrong in version 1.

## Problem

The back-office of the OCR platform needed to manage document types and score parameters.

## Solution

Serverless API with an authorizer and one function per resource, persisting to DynamoDB. Small, cheap and easy to evolve.

### Document OCR — asynchronous API v2

1. Back-office calls the API.
2. Authorizer validates the token.
3. One function per resource (CRUD).
4. Persistence in DynamoDB.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/textract-pipeline | Textract cost per processed page | filter and classify before extracting and use only the needed features (text vs forms vs tables) |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |
| aws/sqs-queue | queue requests | long polling and batch sends |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/ocr-de-documentos-v2/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
