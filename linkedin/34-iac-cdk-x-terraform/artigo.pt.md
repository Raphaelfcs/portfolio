# IaC: CDK x Terraform

*O mesmo fluxo trunk-based em CDK e em Terraform, de engine a workload.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![IaC: mesmo fluxo em CDK e em Terraform](https://raphaelfcs.github.io/portfolio/artigos/img/iac-cdk-x-terraform-pt-1.webp)

> **Em resumo:** CDK ou Terraform? Fiz o mesmo ambiente nos dois.

## O problema

Discussão recorrente no time sobre qual ferramenta de IaC adotar.

## A solução

Mesmo ambiente nas duas ferramentas, lado a lado. A escolha passou a ser sobre o time e o ecossistema, não sobre gosto.

### IaC: mesmo fluxo em CDK e em Terraform

1. Time parte do boilerplate e faz commit.
2. Revisão obrigatória.
3. Pipeline valida e gera o plano.
4. Plan (Terraform) ou synth (CDK).
5. Entrega em ~15 minutos por ambiente.

## O código

```hcl
module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
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

**Módulos Terraform usados:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/iac-cdk-x-terraform/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
