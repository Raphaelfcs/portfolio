# GKE seguro de ponta a ponta

*Laboratório de GKE privado com Workload Identity, Cloud SQL privado, Pub/Sub e borda com Cloud Armor.*

Raphael Santos · 3 min de leitura · Arquiteturas de referência no Google Cloud (2026)

![1 · Arquitetura e jornada](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-pt-1.webp)

> **Em resumo:** GKE "seguro" é uma lista de decisões, não uma opção no console.

## O problema

Laboratório para mostrar GKE privado de ponta a ponta, da borda ao banco.

## A solução

Cluster privado, Workload Identity (sem chave de service account), Cloud SQL só por IP privado, Cloud Armor na borda e Pub/Sub para desacoplar. A jornada numerada no desenho é a mesma que o código implementa.

![Figura 2: 2 · Fundação e IAM](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-pt-2.webp)
*Figura 2: 2 · Fundação e IAM*

![Figura 3: 3 · Estrutura Terraform](https://raphaelfcs.github.io/portfolio/artigos/img/gke-seguro-pt-3.webp)
*Figura 3: 3 · Estrutura Terraform*

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

**Módulos Terraform usados:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/gke-private](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/gke-private), [gcp/cloud-sql](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/cloud-sql), [gcp/pubsub](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/pubsub), [gcp/edge-load-balancer](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/edge-load-balancer)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| gcp/gke-private | nós do GKE (ou pods no Autopilot) | Autopilot para pagar por pod, Spot VMs e CUDs para a base |
| gcp/cloud-sql | vCPU/memória e HA do Cloud SQL | dimensionar pela métrica, CUD para PRD e parar não produtivos |
| gcp/vpc-network | Cloud NAT e tráfego entre zonas/regiões | Private Google Access e manter tráfego na mesma região |
| gcp/project-foundation | custo nasce em projetos sem dono | labels em todo projeto (o módulo já aplica) e orçamento com alerta no Billing |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/google-cloud/gke-seguro/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
