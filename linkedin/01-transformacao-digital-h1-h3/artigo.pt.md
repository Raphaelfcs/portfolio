# Evolução de arquitetura em três horizontes

*Roteiro de modernização em três horizontes (estabilizar, integrar, inovar) para uma empresa de médio porte com sistemas legados.*

Raphael Santos · 3 min de leitura · Estudos de caso de arquitetura (2026)

![Case 1 — Arquitetura de evolução (H1, H2, H3)](https://raphaelfcs.github.io/portfolio/artigos/img/transformacao-digital-h1-h3-pt-1.webp)

> **Em resumo:** Modernizar tudo de uma vez costuma dar errado. Eu prefiro três horizontes.

## O problema

Empresa de médio porte com sistemas legados, pouca automação e um time pequeno de infraestrutura.

## A solução

H1 estabiliza (contas, guardrails, backup), H2 integra (rede, containers, dados) e H3 inova. Cada horizonte entrega valor sozinho, e o próximo só começa quando o anterior está estável.

## O código

```hcl
module "organizations_scp" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/organizations-scp"

  allowed_regions        = ["sa-east-1", "us-east-1"]
  required_tags          = ["CentroCusto", "Ambiente", "Dono"]
  create_tag_enforcement = ["CentroCusto"]
  attach_target          = ["Workloads", "Sandbox"]
  tags                   = local.tags
}

module "security_baseline" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/security-baseline"

  tags = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/eks-cluster](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eks-cluster), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eks-cluster | nós do EKS (EC2) e o control plane por cluster | autoscaling de nós (Karpenter/Cluster Autoscaler), Spot para cargas tolerantes e Savings Plans para a base |
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/backup-plan | retenção de recovery points | retenção por criticidade e cold storage para cópias longas |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/estudos-de-caso/transformacao-digital-h1-h3/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
