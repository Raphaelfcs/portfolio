# Automação de rotina operacional com IA

*Evento no S3 aciona Lambda, Textract, Rekognition e Comprehend; resultado no DynamoDB com API.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Automação de rotina operacional com IA](https://raphaelfcs.github.io/portfolio/artigos/img/automacao-rgs-pt-1.webp)

> **Em resumo:** Rotina operacional manual é candidata natural a uma Lambda agendada.

## O problema

Rotina diária feita à mão, com planilhas e conferência visual.

## A solução

Agendamento, Lambda e S3 resolveram. O ganho não foi só tempo: a rotina passou a ter log e alerta de falha.

### Automação de rotina operacional com IA

1. Arquivo chega no S3.
2. Evento aciona a Lambda.
3. Textract extrai texto; Rekognition analisa imagens.
4. Comprehend classifica o conteúdo.
5. Resultado no DynamoDB.
6. Consulta por API.

## O código

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

## Discussão

**Módulos Terraform usados:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/textract-pipeline | custo por página processada no Textract | filtrar e classificar antes de extrair e usar só as features necessárias (texto x formulário x tabela) |
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/automacao-rgs/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
