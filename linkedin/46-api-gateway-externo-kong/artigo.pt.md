# Kong externo na DMZ do GKE

*Cloud Armor, LB externo, Kong isolado com network policy e LB interno até os microsserviços.*

Raphael Santos · 3 min de leitura · Rede, gateways e dados no Google Cloud (2024)

![Kong externo na DMZ do GKE: AS-IS x TO-BE](https://raphaelfcs.github.io/portfolio/artigos/img/api-gateway-externo-kong-pt-1.webp)

> **Em resumo:** Kong na DMZ do GKE: AS-IS x TO-BE.

## O problema

Gateway externo exposto sem separação clara entre ambientes.

## A solução

Kong em DMZ, balanceador interno e um GKE por ambiente. O desenho mostra o antes e o depois na mesma página.

### Kong externo na DMZ do GKE: AS-IS x TO-BE

1. Borda com Cloud Armor.
2. LB externo só alcança o Kong na porta 8000.
3. Kong chama o LB interno.
4. Microsserviços isolados por ambiente.

> **Nota:** Namespace do Kong com deny-all de entrada e saída, liberando só o necessário.

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

**Módulos Terraform usados:** [gcp/project-foundation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/project-foundation), [gcp/vpc-network](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/vpc-network), [gcp/gke-private](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/gke-private), [gcp/edge-load-balancer](https://github.com/Raphaelfcs/automacao_terraform/tree/main/gcp/edge-load-balancer)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| gcp/gke-private | nós do GKE (ou pods no Autopilot) | Autopilot para pagar por pod, Spot VMs e CUDs para a base |
| gcp/vpc-network | Cloud NAT e tráfego entre zonas/regiões | Private Google Access e manter tráfego na mesma região |
| gcp/project-foundation | custo nasce em projetos sem dono | labels em todo projeto (o módulo já aplica) e orçamento com alerta no Billing |
| gcp/edge-load-balancer | regras de encaminhamento e Cloud Armor | consolidar regras e usar Cloud CDN para cache |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/consultoria-gcp/api-gateway-externo-kong/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
