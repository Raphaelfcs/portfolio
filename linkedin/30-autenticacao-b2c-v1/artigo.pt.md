# Autenticação B2C — primeira versão

*Primeira versão em EKS com IRSA, Secrets Manager e banco por serviço.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Autenticação B2C — primeira versão em EKS](https://raphaelfcs.github.io/portfolio/artigos/img/autenticacao-b2c-v1-pt-1.webp)

> **Em resumo:** A primeira versão de um serviço explica muito sobre a segunda.

## O problema

Primeira versão do serviço de autenticação B2C.

## A solução

Começou serverless com Cognito, API Gateway e Lambda; a evolução para EKS veio com o volume.

### Autenticação B2C — primeira versão em EKS

1. App chama a API.
2. Gateway encaminha ao serviço no EKS.
3. Pod assume a role por IRSA.
4. Credencial do banco vem do Secrets Manager.
5. Serviço é o único dono dos seus dados.

## O código

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "cognito_user_pool" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/cognito-user-pool"

  name_prefix       = local.name_prefix
  domain_prefix     = "demo-dev-login"
  callback_urls     = ["https://app.example.com/callback"]
  logout_urls       = ["https://app.example.com/"]
  custom_attributes = { tenant_id = 64 }
  roles             = { admin = "Administradores", operador = "Operacao" }
  machine_scopes    = { "pedidos.read" = "Ler pedidos", "pedidos.write" = "Gravar pedidos" }
  service_clients   = { faturamento = ["pedidos.read"] }
  tags              = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |
| aws/cognito-user-pool | usuários ativos por mês (MAU) no Cognito | escolher o tier certo e limpar contas inativas |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |
| aws/api-gateway-lambda | requisições no API Gateway | HTTP API em vez de REST API quando não precisa dos recursos extras, e cache na borda |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/autenticacao-b2c-v1/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
