# EKS para funções de core 5G

*Control plane gerenciado, nós no Outposts, Transit Gateway compartilhado e Local Gateway.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![EKS para funções de core 5G](https://raphaelfcs.github.io/portfolio/artigos/img/eks-core-5g-pt-1.webp)

> **Em resumo:** Funções de core 5G rodando em EKS: rede é o requisito número um.

## O problema

Funções de rede de core 5G migrando para Kubernetes gerenciado.

## A solução

Cluster EKS com subnets dedicadas, Transit Gateway para o tráfego de sinalização e um fluxo de deploy separado para infraestrutura e funções de rede.

### EKS para funções de core 5G

1. Datacenter conecta ao Transit Gateway compartilhado por RAM.
2. Attachment dedicado para a VPC 5GC.
3. Control plane gerenciado com ENIs na VPC.
4. Nós de rede rodam no Outposts.
5. Interfaces OAM, SBI e SCTP saem pelo Local Gateway.

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/transit-gateway-attachment | attachments e GB processados no Transit Gateway | consolidar attachments e manter tráfego de alto volume fora do TGW |
| aws/ecr | imagens antigas acumuladas no ECR | lifecycle policy mantendo só as últimas N imagens por repositório |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/eks-core-5g/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
