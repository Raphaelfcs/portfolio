# Batch processing with AWS Batch

*S3 event submits a Batch job with on-demand compute and output to DynamoDB.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Batch processing with AWS Batch](https://raphaelfcs.github.io/portfolio/artigos/img/processamento-em-lote-en-1.webp)

> **TL;DR:** Batch jobs do not need a server running 24 hours.

## Problem

Nightly processing on machines that sat idle all day.

## Solution

An S3 event goes through EventBridge and submits an AWS Batch job: compute exists only while there is work.

### Batch processing with AWS Batch

1. File lands in S3.
2. Event reaches EventBridge.
3. Rule submits the job.
4. Batch provisions compute only for the job.
5. Output saved to DynamoDB; failures are retried.

## The code

```hcl
module "s3_bucket" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/s3-bucket"

  bucket_name = "demo-dev-dados-123456789012"
  tags        = local.tags
}

module "eventbridge_bus_sqs" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/eventbridge-bus-sqs"

  name_prefix             = local.name_prefix
  queue_name              = "pedidos"
  event_sources           = ["parceiro.pedidos"]
  detail_types            = ["PedidoConcluido"]
  producer_principal_arns = ["arn:aws:iam::210987654321:role/parceiro-eventbridge"]
  kms_key_arn             = "arn:aws:kms:sa-east-1:123456789012:key/11111111-2222-3333-4444-555555555555"
  consumer_role_name      = "demo-dev-consumidor"
  alarm_actions           = ["arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"]
  tags                    = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/eventbridge-bus-sqs | published custom events | group events and filter in the rule |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/processamento-em-lote/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
