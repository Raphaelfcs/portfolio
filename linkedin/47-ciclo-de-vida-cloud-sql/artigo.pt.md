# Ciclo de vida de dados do Cloud SQL

*Leitura e escrita separadas, expurgo para Cloud Storage por idade e consulta histórica no BigQuery.*

Raphael Santos · 3 min de leitura · Rede, gateways e dados no Google Cloud (2024)

![Ciclo de vida de dados do Cloud SQL](https://raphaelfcs.github.io/portfolio/artigos/img/ciclo-de-vida-cloud-sql-pt-1.webp)

> **Em resumo:** Banco transacional não é lugar para dado de 10 anos atrás.

## O problema

Cloud SQL crescendo sem parar com dados históricos raramente consultados.

## A solução

Ano corrente no Cloud SQL, expurgo para Cloud Storage com classes por idade e consulta histórica no BigQuery.

### Ciclo de vida de dados do Cloud SQL

1. Escrita no primário.
2. Leitura na réplica com o ano corrente.
3. Expurgo anual para o Cloud Storage.
4. Classes de armazenamento por idade.
5. BigQuery consulta o histórico sem voltar ao banco.

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

**Módulos Terraform usados:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/cloud-sql](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/cloud-sql)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| gcp/cloud-sql | vCPU/memória e HA do Cloud SQL | dimensionar pela métrica, CUD para PRD e parar não produtivos |
| gcp/vpc-network | Cloud NAT e tráfego entre zonas/regiões | Private Google Access e manter tráfego na mesma região |
| gcp/project-foundation | custo nasce em projetos sem dono | labels em todo projeto (o módulo já aplica) e orçamento com alerta no Billing |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/consultoria-gcp/ciclo-de-vida-cloud-sql/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
