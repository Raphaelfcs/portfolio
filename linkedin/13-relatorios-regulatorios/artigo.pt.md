# Relatórios regulatórios assíncronos

*Pedido assíncrono com fila, Lambda, integração SOAP com legado na OCI e entrega por link assinado.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Geração de relatórios regulatórios](https://raphaelfcs.github.io/portfolio/artigos/img/relatorios-regulatorios-pt-1.webp)

> **Em resumo:** Relatório regulatório tem prazo. Arquitetura serverless ajuda a não perder.

## O problema

Relatórios exigidos pelo órgão regulador, gerados manualmente e com risco de atraso.

## A solução

API recebe o pedido, fila desacopla, Lambda gera e o S3 entrega com link temporário. Custo perto de zero fora da janela de entrega.

### Geração de relatórios regulatórios

1. Sistema pede o relatório (POST).
2. Serviço registra o pedido e publica na fila.
3. Lambda consome o pedido.
4. Chama o legado SOAP na OCI para gerar o relatório.
5. Salva o arquivo no S3 e atualiza o estado.
6. Consulta (GET) devolve "processando" ou o link assinado.

## O código

```hcl
module "s3_bucket" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/s3-bucket"

  bucket_name = "demo-dev-dados-123456789012"
  tags        = local.tags
}

module "sqs_queue" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/sqs-queue"

  name_prefix = "demo-dev-"
  queues      = ["pedidos", "notificacoes"]
  tags        = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/sqs-queue | requisições nas filas | long polling e envio em lote |
| aws/api-gateway-lambda | requisições no API Gateway | HTTP API em vez de REST API quando não precisa dos recursos extras, e cache na borda |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/relatorios-regulatorios/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
