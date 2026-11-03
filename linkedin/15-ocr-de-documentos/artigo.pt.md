# OCR de documentos em escala

*Textract assíncrono, validações em Step Functions, resultados no DynamoDB e API de consulta.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![OCR de documentos em escala](https://raphaelfcs.github.io/portfolio/artigos/img/ocr-de-documentos-pt-1.webp)

> **Em resumo:** OCR em escala: DEV, HML e PRD com o mesmo código e custos bem diferentes.

## O problema

Extração de dados de contratos em volume, com picos e necessidade de auditoria.

## A solução

Textract para extração, IA generativa para interpretação, filas para absorver picos e um ambiente por conta. A nova API nasceu desse desenho.

### OCR de documentos em escala

1. Documento entra pela API.
2. Lambda grava no S3.
3. Textract processa de forma assíncrona.
4. SNS avisa quando o job termina.
5. Lambdas extraem campos e classificam o tipo.
6. Validações textual, visual e estrutural.
7. Resultado no DynamoDB, exposto por API.

> **Nota:** Erros vão para um tópico próprio com reprocessamento; ambientes em contas separadas.

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/textract-pipeline | custo por página processada no Textract | filtrar e classificar antes de extrair e usar só as features necessárias (texto x formulário x tabela) |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/cognito-user-pool | usuários ativos por mês (MAU) no Cognito | escolher o tier certo e limpar contas inativas |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/ocr-de-documentos/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
