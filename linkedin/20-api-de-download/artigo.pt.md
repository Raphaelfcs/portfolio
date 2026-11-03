# API de download por URL pré-assinada

*Lambda devolve URL pré-assinada e o arquivo sai direto do S3; objetos novos geram notificação.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![API de download sem passar pelo servidor](https://raphaelfcs.github.io/portfolio/artigos/img/api-de-download-pt-1.webp)

> **Em resumo:** Download de arquivo não deveria passar pelo seu servidor.

## O problema

API que servia arquivos grandes e travava em horário de pico.

## A solução

Lambda gera URL pré-assinada e o S3 entrega o arquivo direto ao cliente. A API ficou leve e o tráfego saiu do caminho crítico.

### API de download sem passar pelo servidor

1. Cliente pede o arquivo.
2. API Gateway aciona a Lambda.
3. Lambda devolve URL pré-assinada.
4. Download vai direto do S3.
5. Objetos novos disparam notificação.

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

**Módulos Terraform usados:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/api-gateway-lambda | requisições no API Gateway | HTTP API em vez de REST API quando não precisa dos recursos extras, e cache na borda |
| aws/sns-topic | mensagens e entregas por protocolo | filtros de assinatura para não entregar o que o consumidor descarta |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/api-de-download/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
