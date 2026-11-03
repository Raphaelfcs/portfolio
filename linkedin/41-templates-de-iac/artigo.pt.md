# Portal do desenvolvedor com templates de IaC

*Backstage, templates por tenant/domain/system, PR, aprovação e apply na conta, com exemplo de RDS.*

Raphael Santos · 3 min de leitura · Portal do desenvolvedor e templates de infraestrutura (2024)

![Portal do desenvolvedor com templates de IaC](https://raphaelfcs.github.io/portfolio/artigos/img/templates-de-iac-pt-1.webp)

> **Em resumo:** Portal do desenvolvedor com templates de IaC: do MVP à arquitetura completa.

## O problema

Times pedindo infraestrutura por ticket e esperando dias.

## A solução

Catálogo de templates, repositórios padronizados, CI/CD de infraestrutura e autenticação, com um exemplo completo de RDS.

### Portal do desenvolvedor com templates de IaC

1. Desenvolvedor abre o portal.
2. Escolhe o template e preenche poucos campos.
3. Portal gera o código e abre o PR.
4. PR roda validações; merge na main dispara o deploy.
5. Apply só depois da aprovação, com role assumida.
6. Recurso aparece no catálogo.

### Exemplo: RDS pelo portal (MVP)

1. Primeiro template cria a instância.
2. Runner dentro da VPC aplica o Terraform.
3. Segundo template cria o banco na instância.
4. Credencial vai para o Secrets Manager.

![Figura 2: Exemplo: RDS pelo portal (MVP)](https://raphaelfcs.github.io/portfolio/artigos/img/templates-de-iac-pt-2.webp)
*Figura 2: Exemplo: RDS pelo portal (MVP)*

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

**Módulos Terraform usados:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/plataforma-iac/templates-de-iac/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
