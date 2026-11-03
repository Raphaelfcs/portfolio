# Provisionamento de VMs automatizado

*Catálogo de VM, automação de IP e tarefas de IPAM, DNS e firewall em paralelo.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Provisionamento de VMs: processo atual](https://raphaelfcs.github.io/portfolio/artigos/img/provisionamento-de-vms-pt-1.webp)

> **Em resumo:** Pedido de VM que leva semanas é processo, não tecnologia.

## O problema

Criação de VMs Linux e bancos (PaaS ou IaaS) com várias aprovações manuais.

## A solução

Redesenhei o fluxo e automatizei o que era repetitivo. O critério PaaS x IaaS ficou explícito no desenho.

### Provisionamento de VMs: processo atual

1. O pedido chega numa planilha com mais de 20 campos.
2. Chamado de DNS para definir o hostname.
3. IP buscado à mão no Azure e no IPAM.
4. Regra e NAT no firewall por outra fila.
5. War room de infraestrutura cria a VM por script.
6. DBA instala o banco em IaaS e o SLA estoura.

> **Nota:** Cada fila espera a anterior: semanas para uma VM simples.

### Provisionamento de VMs: processo proposto

1. Pedido nasce de um catálogo com padrões.
2. Automação valida o hostname e busca IP livre.
3. IPAM, DNS e firewall correm em paralelo.
4. VM criada por Terraform.
5. Banco PaaS por padrão; IaaS só com justificativa.

> **Nota:** Padrões do catálogo: disco Standard em dev/hml e Premium em prd, sem IP público, backup e monitoração ligados, tags obrigatórias.
> **Nota:** A VM entra pela esteira de workload do padrão de IaC em monorepo (padrao-iac).

![Figura 2: Provisionamento de VMs: processo proposto](https://raphaelfcs.github.io/portfolio/artigos/img/provisionamento-de-vms-pt-2.webp)
*Figura 2: Provisionamento de VMs: processo proposto*

## O código

```hcl
module "sql_database" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//azure/sql-database"

  server_name                = "sql-demo-dev"
  resource_group_name        = "rg-dados"
  location                   = "brazilsouth"
  entra_admin_login          = "grp-dba"
  entra_admin_object_id      = "00000000-0000-0000-0000-000000000001"
  log_analytics_workspace_id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-monitoria/providers/Microsoft.OperationalInsights/workspaces/law-plataforma"
  databases                  = { cartoes = {}, conciliacao = { sku_name = "GP_Gen5_4", zone_redundant = true } }
  tags                       = local.tags
}

module "monitor_alerts" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//azure/monitor-alerts"

  resource_group_name     = "rg-monitoria"
  action_group_name       = "ag-plataforma"
  action_group_short_name = "plataforma"
  emails                  = ["plataforma@example.com"]
  metric_alerts = {
    cpu-alta = { target_ids = ["/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-app/providers/Microsoft.Compute/virtualMachines/vm-app-01"], metric_namespace = "Microsoft.Compute/virtualMachines", metric_name = "Percentage CPU", threshold = 85 }
    dtu-alta = { target_ids = ["/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-dados/providers/Microsoft.Sql/servers/sql-demo/databases/app"], metric_namespace = "Microsoft.Sql/servers/databases", metric_name = "cpu_percent", threshold = 80, severity = 1 }
  }
  tags = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [azure/sql-database](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/sql-database), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| azure/sql-database | vCores ou DTUs do banco | serverless para cargas intermitentes e reserva para PRD |
| azure/monitor-alerts | alertas e ingestão no Log Analytics | retenção por tabela e alertas de orçamento (Cost Management) |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/provisionamento-de-vms/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
