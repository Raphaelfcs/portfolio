# Plataforma AWS de uma operadora de saúde

*Backup multi-região com rede compartilhada e a evolução do IaC para um state por recurso e ambiente.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Backup multi-região com rede compartilhada](https://raphaelfcs.github.io/portfolio/artigos/img/visao-geral-plataforma-pt-1.webp)

> **Em resumo:** Doze visões de uma mesma plataforma: foi assim que consegui explicar a AWS de uma operadora de saúde.

## O problema

Ambiente grande, com backup, orquestradores em duas regiões, OCI, ECS, EKS e IaC, e cada time conhecendo só um pedaço.

## A solução

Uma página por assunto, todas com a mesma legenda. A visão geral virou o mapa de onboarding de quem chegava no time.

### Backup multi-região com rede compartilhada

1. Agentes de backup rodam junto das cargas, em Auto Scaling.
2. Tráfego de backup passa pelo Transit Gateway da conta de rede (TCP 8400-8410).
3. Orquestrador ativo em us-east-1, passivo em sa-east-1.
4. Gravação no S3 IA por VPC endpoint, sem internet.
5. Lifecycle move cópias antigas para Glacier Deep Archive.
6. Réplica entre regiões para DR.

> **Nota:** Contas separadas para aplicação, rede e backup reduzem o raio de impacto.

### IaC: um state por recurso e por ambiente

1. v0: um state para tudo; qualquer mudança arriscava a infra inteira.
2. v1: pipeline por recurso e ambiente.
3. Cada recurso tem seu backend e seu ciclo de vida.
4. Dependências por outputs e depends_on, nunca por IDs fixos.

![Figura 2: IaC: um state por recurso e por ambiente](https://raphaelfcs.github.io/portfolio/artigos/img/visao-geral-plataforma-pt-2.webp)
*Figura 2: IaC: um state por recurso e por ambiente*

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

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/vpc-endpoints](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc-endpoints), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr), [aws/backup-plan](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/backup-plan)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/transit-gateway-attachment | attachments e GB processados no Transit Gateway | consolidar attachments e manter tráfego de alto volume fora do TGW |
| aws/ecr | imagens antigas acumuladas no ECR | lifecycle policy mantendo só as últimas N imagens por repositório |
| aws/backup-plan | retenção de recovery points | retenção por criticidade e cold storage para cópias longas |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/visao-geral-plataforma/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
