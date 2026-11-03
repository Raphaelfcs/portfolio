# Fundamentos de AWS: identidade e guardrails

*Material de capacitação: Identity Center, OUs, SCPs, boundaries e políticas de recurso.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Fundamentos de AWS: identidade e guardrails](https://raphaelfcs.github.io/portfolio/artigos/img/fundamentos-aws-pt-1.webp)

> **Em resumo:** Material de capacitação também é arquitetura.

## O problema

Time novo precisando de base comum de AWS.

## A solução

Cloud, Well-Architected, IAM, VPC, S3 e guardrails explicados com os mesmos ícones usados nos projetos reais.

### Fundamentos de AWS: identidade e guardrails

1. Acesso humano federado, com MFA, sem usuário IAM.
2. Permission sets por conta.
3. SCP define o teto de cada OU.
4. Boundary limita o que uma role pode delegar.
5. Política de recurso fecha o acesso no próprio recurso.

> **Nota:** Menor privilégio sempre; root protegido com MFA e sem uso diário.

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

module "iam_group" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-group"

  name                = "break-glass"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
  require_mfa         = true
}
```

## Discussão

**Módulos Terraform usados:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/iam-group](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-group), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/fundamentos-aws/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
