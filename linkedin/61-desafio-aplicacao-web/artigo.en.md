# Challenge: scalable web application

*Static site, key-protected serverless API and SNS notification.*

Raphael Santos · 3 min read · Architecture technical challenges

![Challenge: scalable web application](https://raphaelfcs.github.io/portfolio/artigos/img/desafio-aplicacao-web-en-1.webp)

> **TL;DR:** Technical challenge: a scalable web application on AWS.

## Problem

Challenge asking for high availability at the lowest possible cost.

## Solution

Static site on the CDN, key-protected serverless API and SNS notifications. Scales on its own and costs cents when idle.

### Challenge: scalable web application

1. DNS on Route 53.
2. Static site on S3.
3. API with key.
4. Lambda processes.
5. SNS notifies.

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

**Terraform modules used:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/cloudfront-spa | CDN data transfer | good caching and compression; the CDN usually lowers origin egress cost |
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/api-gateway-lambda | API Gateway requests | HTTP API instead of REST API when the extra features are not needed, plus edge caching |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/desafios/desafio-aplicacao-web/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
