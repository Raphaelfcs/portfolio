# Guardrails para S3, RDS e CloudFront

*Controles preventivos por SCP e boundary, detectivos por Config e lifecycle por IaC.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Guardrails para S3, RDS e CloudFront](https://raphaelfcs.github.io/portfolio/artigos/img/guardrails-s3-rds-cloudfront-pt-1.webp)

> **Em resumo:** Guardrail bom é o que impede o erro antes do deploy.

## O problema

Buckets públicos por engano, bancos sem criptografia e distribuições sem TLS mínimo.

## A solução

Controles preventivos com SCP e detectivos com Config/Security Hub para S3, RDS e CloudFront, com uma página por serviço.

### Guardrails para S3, RDS e CloudFront

1. SCPs aplicadas na organização.
2. Buckets sem acesso público e com criptografia.
3. Lifecycle para Glacier por IaC.
4. RDS Multi-AZ, sem exclusão fora do processo.
5. Config detecta distribuições fora do padrão.

> **Nota:** Referências: LGPD, ISO 27001 e ISO 27005.

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

**Módulos Terraform usados:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |
| aws/security-baseline | Config, GuardDuty e Security Hub em todas as contas | gravar no Config só os tipos de recurso relevantes |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/guardrails-s3-rds-cloudfront/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
