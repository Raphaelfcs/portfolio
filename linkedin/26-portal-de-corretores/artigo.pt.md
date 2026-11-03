# Portal de corretores

*SPA no CloudFront, BFF em EKS atrás de NLB e banco com backup testado.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Portal de corretores](https://raphaelfcs.github.io/portfolio/artigos/img/portal-de-corretores-pt-1.webp)

> **Em resumo:** Portal de corretores: front-end estático, API em container e backup testado.

## O problema

Portal web para corretores com picos em campanhas comerciais.

## A solução

CDN na frente, API em EKS, banco gerenciado e plano de backup com restauração testada, não só configurada.

### Portal de corretores

1. Entrada com WAF e Shield.
2. SPA servida pelo CloudFront.
3. API Gateway publica o BFF.
4. NLB entrega ao BFF no EKS.
5. Banco só na rede privada.
6. Backup com restauração testada.

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/cloudfront-spa | transferência de dados da CDN | cache bem configurado e compressão; a CDN costuma reduzir o custo de saída da origem |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/portal-de-corretores/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
