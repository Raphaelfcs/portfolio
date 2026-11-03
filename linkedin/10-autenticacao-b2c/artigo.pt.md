# Autenticação B2C em ECS Fargate

*Login de clientes finais com Cognito, API Gateway e serviço em Fargate com banco privado.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Autenticação B2C em ECS Fargate](https://raphaelfcs.github.io/portfolio/artigos/img/autenticacao-b2c-pt-1.webp)

> **Em resumo:** Autenticação de cliente final é o serviço que não pode cair.

## O problema

Login de clientes finais com picos de acesso e integração com sistemas legados.

## A solução

Zoom-out para o negócio entender o fluxo, zoom-in para o time entender rede e dependências. Cognito tira de nós o problema de guardar senha.

### Autenticação B2C em ECS Fargate

1. Cliente acessa pela borda com WAF.
2. Front-end SPA servido pelo CloudFront.
3. Login e tokens pelo Cognito.
4. API Gateway valida a chave e o token.
5. ALB entrega à task no Fargate.
6. Serviço lê e grava no RDS privado.

> **Nota:** Imagem vem do ECR compartilhado; logs vão para a conta de observabilidade.

## O código

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "vpc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/vpc"

  name_prefix        = local.name_prefix
  cidr_block         = "10.20.0.0/16"
  azs                = ["sa-east-1a", "sa-east-1b"]
  single_nat_gateway = true
  eks_cluster_name   = "demo-dev"
  tags               = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/cloudfront-spa | transferência de dados da CDN | cache bem configurado e compressão; a CDN costuma reduzir o custo de saída da origem |
| aws/lambda-function | duração x memória das funções | ajustar memória com Power Tuning e usar arm64 |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/autenticacao-b2c/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
