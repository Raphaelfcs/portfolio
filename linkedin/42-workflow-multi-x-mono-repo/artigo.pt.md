# Workflow de templates: multi-repo x monorepo

*Repositórios de aplicação e de infra, CI/CD e Atlantis, comparados ao monorepo.*

Raphael Santos · 3 min de leitura · Portal do desenvolvedor e templates de infraestrutura (2024)

![Workflow de templates: multi-repo x monorepo](https://raphaelfcs.github.io/portfolio/artigos/img/workflow-multi-x-mono-repo-pt-1.webp)

> **Em resumo:** Templates de IaC: multi-repo ou monorepo?

## O problema

Plataforma de templates precisando decidir a organização dos repositórios.

## A solução

Visão macro do workflow e as duas opções desenhadas lado a lado, com prós e contras de cada uma.

### Workflow de templates: multi-repo x monorepo

1. Desenvolvedor escolhe o template.
2. Portal cria os repositórios.
3. CI constrói e publica a imagem.
4. CD faz o deploy no ECS.
5. Infra separada, aplicada pelo Atlantis.

> **Nota:** No monorepo, app e terraform/ ficam no mesmo repositório com pipelines separados.

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

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/workflow-multi-x-mono-repo/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
