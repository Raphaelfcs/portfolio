# Document OCR at scale

*Asynchronous Textract, validations in Step Functions, results in DynamoDB and a query API.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Document OCR at scale](https://raphaelfcs.github.io/portfolio/artigos/img/ocr-de-documentos-en-1.webp)

> **TL;DR:** OCR at scale: same code for DEV, HML and PRD, very different costs.

## Problem

High-volume contract data extraction, with peaks and audit requirements.

## Solution

Asynchronous Textract, SNS when the job ends, Lambdas that extract and classify, validations in Step Functions and results in DynamoDB behind an API. Errors go to their own topic with reprocessing.

### Document OCR at scale

1. Document enters through the API.
2. Lambda stores it in S3.
3. Textract processes asynchronously.
4. SNS signals when the job is done.
5. Lambdas extract fields and classify the type.
6. Textual, visual and structural validations.
7. Result in DynamoDB, exposed via API.

> **Note:** Errors go to their own topic with reprocessing; environments in separate accounts.

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

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/textract-pipeline | Textract cost per processed page | filter and classify before extracting and use only the needed features (text vs forms vs tables) |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/cognito-user-pool | Cognito monthly active users (MAU) | pick the right tier and clean up inactive accounts |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/ocr-de-documentos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
