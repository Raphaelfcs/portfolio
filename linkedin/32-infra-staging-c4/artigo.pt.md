# Infra de staging em C4

*Contexto C4 da plataforma e o modelo de permissões do IaC com quatro identidades separadas.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Infra de staging — contexto (C4 nível 1)](https://raphaelfcs.github.io/portfolio/artigos/img/infra-staging-c4-pt-1.webp)

> **Em resumo:** C4 Model para infraestrutura: funciona, e muito bem.

## O problema

Ambiente de staging com várias stacks e fronteiras de state pouco claras.

## A solução

Cinco níveis: contexto, fronteiras de state, rede e security groups, permissões do IaC e gates do pipeline. Cada nível é uma pergunta de revisão.

### Infra de staging — contexto (C4 nível 1)

1. Acesso pela CDN e ALB.
2. Cargas no cluster de workload.
3. Eventos publicados no Kafka gerenciado.
4. Pinot consulta em tempo real.
5. Dados transacionais e cache em sub-redes privadas.
6. Sistemas da operadora chegam pelo Transit Gateway.

### Permissões do IaC: quatro identidades que não se cruzam

1. Só o operador aplica infra, depois de revisar o plan.
2. CI publica imagem e nada além.
3. ArgoCD puxa o estado do git (pull-based).
4. Pods leem só o prefixo de segredo deles.

![Figura 2: Permissões do IaC: quatro identidades que não se cruzam](https://raphaelfcs.github.io/portfolio/artigos/img/infra-staging-c4-pt-2.webp)
*Figura 2: Permissões do IaC: quatro identidades que não se cruzam*

## O código

```hcl
module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}

module "iam_github_oidc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-github-oidc"

  github_org           = "minha-org"
  github_repo          = "infra"
  allowed_environments = ["dev", "prd"]
  managed_role_prefix  = "app-"
  state_bucket_arn     = "arn:aws:s3:::demo-tfstate-123456789012"
  tags                 = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/elasticache-redis | nós do ElastiCache ligados 24h | tipo de nó menor com Graviton e reserva para PRD |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/infra-staging-c4/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
