# Processamento em lote com AWS Batch

*Evento no S3 dispara job no Batch com computação sob demanda e saída no DynamoDB.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Processamento em lote com AWS Batch](https://raphaelfcs.github.io/portfolio/artigos/img/processamento-em-lote-pt-1.webp)

> **Em resumo:** Job em lote não precisa de servidor ligado 24 horas.

## O problema

Processamentos noturnos rodando em máquinas que ficavam ociosas o dia todo.

## A solução

Prova de conceito com AWS Batch acionado por evento: o cluster existe só enquanto há trabalho.

### Processamento em lote com AWS Batch

1. Arquivo chega no S3.
2. Evento aciona o EventBridge.
3. Regra submete o job.
4. Batch provisiona a computação só durante o job.
5. Saída gravada no DynamoDB; falhas são reprocessadas.

## O código

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

## Discussão

**Módulos Terraform usados:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/eventbridge-bus-sqs | eventos customizados publicados | agrupar eventos e filtrar na regra |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/processamento-em-lote/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
