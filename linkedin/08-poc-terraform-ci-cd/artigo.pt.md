# POC de Terraform com CI/CD no Google Cloud

*GitHub Actions com Workload Identity Federation, uma service account por ambiente e state remoto.*

Raphael Santos · 3 min de leitura · Arquiteturas de referência no Google Cloud (2026)

![POC de Terraform com CI/CD no Google Cloud](https://raphaelfcs.github.io/portfolio/artigos/img/poc-terraform-ci-cd-pt-1.webp)

> **Em resumo:** POC de Terraform com CI/CD no Google Cloud.

## O problema

Prova de conceito para validar pipeline de IaC antes de adotar em produção.

## A solução

State remoto, pipeline por ambiente e projeto isolado para a POC.

### POC de Terraform com CI/CD no Google Cloud

1. PR obrigatório, sem push direto.
2. CI roda lint, testes e plan.
3. Sem chave JSON: OIDC do GitHub.
4. Uma service account por ambiente.
5. Apply e smoke test; acesso público fechado à noite.

## O código

```hcl
module "project_foundation" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//gcp/project-foundation"

  project_id       = "demo-plataforma-dev"
  project_name     = "Demo Plataforma"
  billing_account  = "000000-000000-000000"
  apis             = ["compute.googleapis.com", "container.googleapis.com", "sqladmin.googleapis.com"]
  boolean_policies = ["compute.skipDefaultNetworkCreation", "iam.disableServiceAccountKeyCreation", "storage.uniformBucketLevelAccess"]
  labels           = local.labels
}

module "vpc_network" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//gcp/vpc-network"

  project_id = module.project_foundation.project_id
  region     = local.region
  subnet     = { name = "sn-gke-sp", cidr = "10.10.0.0/20", pods_cidr = "10.20.0.0/16", services_cidr = "10.30.0.0/20" }
  psa_range  = { address = "10.40.0.0", prefix_length = 16 }
}
```

## Discussão

**Módulos Terraform usados:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| gcp/vpc-network | Cloud NAT e tráfego entre zonas/regiões | Private Google Access e manter tráfego na mesma região |
| gcp/project-foundation | custo nasce em projetos sem dono | labels em todo projeto (o módulo já aplica) e orçamento com alerta no Billing |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/google-cloud/poc-terraform-ci-cd/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
