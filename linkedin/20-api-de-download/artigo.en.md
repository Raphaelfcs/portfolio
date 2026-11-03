# Download API with pre-signed URLs

*Lambda returns a pre-signed URL and the file comes straight from S3; new objects trigger a notification.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Download API that bypasses the server](https://raphaelfcs.github.io/portfolio/artigos/img/api-de-download-en-1.webp)

> **TL;DR:** File downloads should not go through your server.

## Problem

API that served large files and choked at peak hours.

## Solution

Lambda returns a pre-signed URL and S3 delivers the file straight to the client. The API got light and the traffic left the critical path.

### Download API that bypasses the server

1. Client asks for the file.
2. API Gateway invokes Lambda.
3. Lambda returns a pre-signed URL.
4. Download goes straight from S3.
5. New objects trigger a notification.

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

**Terraform modules used:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/api-gateway-lambda | API Gateway requests | HTTP API instead of REST API when the extra features are not needed, plus edge caching |
| aws/sns-topic | messages and deliveries per protocol | subscription filters so consumers do not receive what they discard |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/api-de-download/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
