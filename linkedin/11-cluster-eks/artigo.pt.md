# Cluster EKS compartilhado

*Cluster multi-tenant com namespace por aplicação, HPA, quotas e serviços compartilhados.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Cluster EKS compartilhado da plataforma](https://raphaelfcs.github.io/portfolio/artigos/img/cluster-eks-pt-1.webp)

> **Em resumo:** Um cluster EKS compartilhado precisa de regras claras antes do primeiro deploy.

## O problema

Várias aplicações migrando para um mesmo cluster EKS.

## A solução

Subnets privadas, nós gerenciados, imagens só do ECR e chave KMS para segredos. O desenho de detalhe evitou discussões sobre "onde fica cada coisa".

### Cluster EKS compartilhado da plataforma

1. Borda com CloudFront e WAF.
2. API Gateway publica as rotas.
3. VPC link até o NLB interno.
4. Ingress roteia por namespace (multi-tenant).
5. Cada app usa a própria fila e banco.

> **Nota:** Namespace por aplicação com HPA, limits e quotas; afinidade por label separa tenants.

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/ecr | imagens antigas acumuladas no ECR | lifecycle policy mantendo só as últimas N imagens por repositório |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/cluster-eks/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
