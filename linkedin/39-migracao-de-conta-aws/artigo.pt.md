# Migração de workload entre contas AWS

*Topologia, dependência de identidade e achados que orientam a mudança de organização.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Migração de workload entre contas AWS](https://raphaelfcs.github.io/portfolio/artigos/img/migracao-de-conta-aws-pt-1.webp)

> **Em resumo:** Migrar workload entre contas AWS: topologia, custos e achados.

## O problema

Workload rodando fora da organização da empresa.

## A solução

Três páginas: topologia atual, custos e achados que mudam a decisão. A migração ficou baseada em evidência.

### Migração de workload entre contas AWS

1. Hoje todo acesso humano depende do Identity Center da organização atual.
2. Na organização da empresa, SCPs e guardrails já existem.
3. A VPC passa a usar a rede compartilhada.

> **Nota:** Sair da organização sem usuário de emergência tranca a conta: criar acesso break-glass antes.
> **Nota:** Nada fora de sa-east-1, sem Route 53 e sem ACM: menos coisas a migrar.

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

module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/transit-gateway-attachment | attachments e GB processados no Transit Gateway | consolidar attachments e manter tráfego de alto volume fora do TGW |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/migracao-de-conta-aws/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
