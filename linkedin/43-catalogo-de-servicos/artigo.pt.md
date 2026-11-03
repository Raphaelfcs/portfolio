# Catálogo de serviços self-service

*Do pedido no Backstage ao recurso criado na conta, com credencial no Secrets Manager.*

Raphael Santos · 3 min de leitura · Portal do desenvolvedor e templates de infraestrutura (2024)

![Catálogo de serviços self-service](https://raphaelfcs.github.io/portfolio/artigos/img/catalogo-de-servicos-pt-1.webp)

> **Em resumo:** Self-service de infraestrutura começa no catálogo.

## O problema

Desenvolvedores sem caminho padrão para pedir recursos.

## A solução

Do catálogo ao provisionamento: o desenvolvedor escolhe, o pipeline valida e a nuvem entrega.

### Catálogo de serviços self-service

1. Desenvolvedor pede no catálogo.
2. Portal grava o código no Git.
3. Pipeline aplica.
4. Banco criado na conta.
5. Credencial no Secrets Manager.

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

**Módulos Terraform usados:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/s3-bucket | armazenamento e versões antigas no S3 | lifecycle para IA/Glacier e expiração de versões não atuais |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/catalogo-de-servicos/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
