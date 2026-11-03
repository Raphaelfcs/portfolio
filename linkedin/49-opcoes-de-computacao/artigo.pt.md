# Opções de computação: ECS, EKS e Beanstalk

*A mesma aplicação de benefícios desenhada nas três opções, com a mesma borda e o mesmo banco.*

Raphael Santos · 3 min de leitura · Plataforma de benefícios em AWS (2023)

![Mesma aplicação em ECS Fargate](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-pt-1.webp)

> **Em resumo:** ECS Fargate, EKS ou Beanstalk? Desenhei os três para a mesma aplicação.

## O problema

Plataforma de benefícios saindo de servidores tradicionais.

## A solução

Três desenhos com a mesma borda (CDN/WAF), mesmo registry e mesmo banco. A comparação ficou justa e a decisão, documentada.

### Mesma aplicação em ECS Fargate

1. Borda com CloudFront e WAF.
2. ALB distribui entre tasks.
3. Banco e cache privados.

### Mesma aplicação em EKS

1. Mesma borda.
2. Ingress separa API e web por namespace.
3. Mesmos dados privados.

### Mesma aplicação em Elastic Beanstalk

1. Mesma borda.
2. Leitura e escrita separadas.
3. Jobs isolados para escalar horizontalmente.

> **Nota:** As três versões usam a mesma borda, registry e banco: a comparação fica justa.

![Figura 2: Mesma aplicação em EKS](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-pt-2.webp)
*Figura 2: Mesma aplicação em EKS*

![Figura 3: Mesma aplicação em Elastic Beanstalk](https://raphaelfcs.github.io/portfolio/artigos/img/opcoes-de-computacao-pt-3.webp)
*Figura 3: Mesma aplicação em Elastic Beanstalk*

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/elasticache-redis | nós do ElastiCache ligados 24h | tipo de nó menor com Graviton e reserva para PRD |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/beneficios/opcoes-de-computacao/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
