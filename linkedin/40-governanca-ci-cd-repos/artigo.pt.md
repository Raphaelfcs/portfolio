# Governança de CI/CD para repositórios Terraform

*Boilerplate, merge request revisado pelo CCoE e apply com identidade federada.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Governança de CI/CD dos repositórios Terraform](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-ci-cd-repos-pt-1.webp)

> **Em resumo:** Governança de CI/CD para repositórios Terraform.

## O problema

Vários times aplicando Terraform sem padrão de aprovação.

## A solução

Pipeline com plano, aprovação e aplicação controlados pelo CCoE, com identidade federada no lugar de chaves.

### Governança de CI/CD dos repositórios Terraform

1. Time parte do boilerplate.
2. Cria o repositório do workload.
3. Merge request revisado pelo CCoE.
4. Aprovado, o pipeline roda.
5. Aplica nas contas com identidade federada.

## O código

```hcl
module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}

module "iam_github_oidc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-github-oidc"

  github_org           = "minha-org"
  github_repo          = "infra"
  allowed_environments = ["dev", "prd"]
  managed_role_prefix  = "app-"
  state_bucket_arn     = "arn:aws:s3:::demo-tfstate-123456789012"
  tags                 = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | recursos sem dono e ambientes não produtivos ligados 24h | tags obrigatórias e desligamento fora do horário |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/governanca-ci-cd-repos/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
