# EventBridge and Lambda: cross-account integration that survives failure

*A dedicated bus, a queue with a DLQ, an archive for replay and alarms that fire before the customer notices.*

Raphael Santos · 4 min read · Hands-on AWS

![aws/eventbridge-bus-sqs: Cross-account event bus -> SQS](https://raphaelfcs.github.io/portfolio/artigos/img/aws-eventbridge-lambda-en-1.webp)

> **TL;DR:** Event-driven integration is only reliable when you know what happens to the message that failed. Without a DLQ, an archive and alarms, the event simply disappears.

## Problem

A producer in another account (a partner, another team) needs to tell your system that something happened. The first version is usually a direct HTTP call: when the consumer is down, the event is lost and nobody notices until a customer complains.

## Solution

The producer publishes to a dedicated EventBridge bus, opened by resource policy only to its roles. A rule filters by source and detail-type and delivers into an SQS queue encrypted with KMS, with a DLQ for the rule and for the queue. The archive keeps events and allows replay without depending on the producer. Lambdas consume the queue with least privilege, a DLQ and X-Ray, and alarms cover a stopped consumer, old messages, a non-empty DLQ and rule delivery failures.

### How to build it

1. Create one bus per integration domain and allow PutEvents only for the producer’s roles.
2. Filter in the rule by source and detail-type; do not make the consumer figure out what to ignore.
3. Deliver into an encrypted SQS queue, with a DLQ on the rule (delivery failure) and on the queue (processing failure).
4. Turn on the archive with a defined retention so you can reprocess after a bug.
5. Consume with a least-privilege Lambda, a tuned batch size and partial batch failure reporting.
6. Alarm on the age of the oldest message, DLQ depth and the rule’s FailedInvocations.

> **Note:** For scheduled tasks I use EventBridge Scheduler, which supports time zones: 7 a.m. in São Paulo stays 7 a.m. through another country’s daylight saving change.

![Figure 2: aws/lambda-function: Packaged Lambda function](https://raphaelfcs.github.io/portfolio/artigos/img/aws-eventbridge-lambda-en-2.webp)
*Figure 2: aws/lambda-function: Packaged Lambda function*

## The code

```hcl
module "eventbridge_bus_sqs" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/eventbridge-bus-sqs?ref=main"

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

**Terraform modules used:** [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/eventbridge-bus-sqs | Events published to a custom bus and GB archived. | Filter at the source and set the archive retention. |
| aws/lambda-function | GB-seconds of execution and logs without retention. | Memory tuned by measurement and a log group with retention and KMS. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/eventbridge-bus-sqs/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
