# Pipeline de deploy por ambiente

*Imagem construída uma vez a partir de template e promovida de DEV a PRD.*

Raphael Santos · 3 min de leitura · Plataforma de benefícios em AWS (2023)

![Pipeline de deploy por ambiente](https://raphaelfcs.github.io/portfolio/artigos/img/pipeline-de-deploy-pt-1.webp)

> **Em resumo:** Pipeline por ambiente começa no template da imagem.

## O problema

Deploys manuais e imagens diferentes em cada ambiente.

## A solução

Imagem gerada uma vez a partir de template, publicada no registry e promovida para DEV, HML e PRD.

### Pipeline de deploy por ambiente

1. Template padroniza a imagem.
2. Pipeline publica no ECR.
3. Deploy em DEV.
4. Mesma imagem promovida para QA.
5. PRD com aprovação.

## O código

```hcl
module "iam_github_oidc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-github-oidc"

  github_org           = "minha-org"
  github_repo          = "infra"
  allowed_environments = ["dev", "prd"]
  managed_role_prefix  = "app-"
  state_bucket_arn     = "arn:aws:s3:::demo-tfstate-123456789012"
  tags                 = local.tags
}

module "ecr" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/ecr"

  name_prefix      = "demo"
  repository_names = ["api", "worker"]
  tags             = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/ecr](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/ecr)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/ecr | imagens antigas acumuladas no ECR | lifecycle policy mantendo só as últimas N imagens por repositório |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/beneficios/pipeline-de-deploy/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
