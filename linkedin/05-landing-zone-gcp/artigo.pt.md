# Landing zone no Google Cloud

*Landing zone completa em dez visões: hierarquia, conectividade, GKE e Cloud Run, segurança de dados, DevOps, migração, APIs, web e storage.*

Raphael Santos · 3 min de leitura · Arquiteturas de referência no Google Cloud (2026)

![1 · Landing zone (árvore de recursos)](https://raphaelfcs.github.io/portfolio/artigos/img/landing-zone-gcp-pt-1.webp)

> **Em resumo:** Landing zone não é só criar projetos: são seis decisões que precisam conversar entre si.

## O problema

Uma landing zone completa no Google Cloud: hierarquia, conectividade, GKE e Cloud Run, dados, DevOps e observabilidade.

## A solução

Separei o desenho em uma página por decisão. Cada página responde a uma pergunta do comitê de arquitetura e aponta para o módulo Terraform que a implementa.

![Figura 2: 2 · Conectividade](https://raphaelfcs.github.io/portfolio/artigos/img/landing-zone-gcp-pt-2.webp)
*Figura 2: 2 · Conectividade*

![Figura 3: 3 · GKE e Cloud Run](https://raphaelfcs.github.io/portfolio/artigos/img/landing-zone-gcp-pt-3.webp)
*Figura 3: 3 · GKE e Cloud Run*

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

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/google-cloud/landing-zone-gcp/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
