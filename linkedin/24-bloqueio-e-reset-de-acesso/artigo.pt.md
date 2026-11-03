# Bloqueio e reset de acesso compartilhado

*Serviço em EKS consumido por sistemas na AWS e na OCI via Transit Gateway e VPN.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Bloqueio e reset de acesso compartilhado](https://raphaelfcs.github.io/portfolio/artigos/img/bloqueio-e-reset-de-acesso-pt-1.webp)

> **Em resumo:** Serviço compartilhado entre AWS e OCI: a rede é metade do projeto.

## O problema

Bloqueio e reset de credenciais usado por vários sistemas, alguns fora da AWS.

## A solução

Componentes em EKS e ECS, Transit Gateway e VPN site-to-site até a OCI. O desenho por nuvem ajudou a negociar regras de firewall.

### Bloqueio e reset de acesso compartilhado

1. Portais chamam o serviço pela borda.
2. API Gateway até o EKS.
3. Saída pelo Transit Gateway da conta de rede.
4. VPN até os sistemas na OCI.

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/vpn-site-to-site](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpn-site-to-site)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/transit-gateway-attachment | attachments e GB processados no Transit Gateway | consolidar attachments e manter tráfego de alto volume fora do TGW |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/bloqueio-e-reset-de-acesso/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
