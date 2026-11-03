# Desafio: API serverless

*API Gateway + Lambda em sub-rede privada, tudo em Terraform.*

Raphael Santos · 3 min de leitura · Desafios técnicos de arquitetura

![Desafio: API serverless com IaC](https://raphaelfcs.github.io/portfolio/artigos/img/desafio-api-serverless-pt-1.webp)

> **Em resumo:** Desafio técnico: uma API serverless com IaC do zero.

## O problema

Desafio de entrevista pedindo API funcional, segura e reproduzível.

## A solução

API Gateway + Lambda, tudo em Terraform. Simples de entender e de destruir no final.

### Desafio: API serverless com IaC

1. Usuário chama a rota.
2. Gateway invoca a Lambda.
3. Saída para a internet via NAT, se precisar.

## O código

```hcl
module "lambda_function" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/lambda-function"

  function_name       = "demo-dev-relatorio"
  source_dir          = "${path.module}/src"
  schedule_expression = "rate(1 day)"
  environment         = { NIVEL_LOG = "INFO" }
  tags                = local.tags
}

module "api_gateway_lambda" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/api-gateway-lambda"

  name                 = "demo-dev-api"
  lambda_function_name = module.lambda_function.function_name
  lambda_invoke_arn    = module.lambda_function.invoke_arn
  tags                 = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/api-gateway-lambda | requisições no API Gateway | HTTP API em vez de REST API quando não precisa dos recursos extras, e cache na borda |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/desafios/desafio-api-serverless/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
