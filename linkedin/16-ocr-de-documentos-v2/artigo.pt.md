# OCR de documentos — API v2

*Back-office serverless com authorizer e uma função por recurso.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![OCR de documentos — API v2 assíncrona](https://raphaelfcs.github.io/portfolio/artigos/img/ocr-de-documentos-v2-pt-1.webp)

> **Em resumo:** A versão 2 de uma API costuma ser sobre o que deu errado na versão 1.

## O problema

A primeira API de OCR era síncrona e sofria com documentos grandes.

## A solução

Processamento assíncrono: o cliente envia, recebe um ID e consulta o status. Timeouts sumiram e o custo ficou previsível.

### OCR de documentos — API v2 assíncrona

1. Back-office chama a API.
2. Authorizer valida o token.
3. Uma função por recurso (CRUD).
4. Persistência no DynamoDB.

## O código

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

## Discussão

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/textract-pipeline | custo por página processada no Textract | filtrar e classificar antes de extrair e usar só as features necessárias (texto x formulário x tabela) |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |
| aws/sqs-queue | requisições nas filas | long polling e envio em lote |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/ocr-de-documentos-v2/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
