# Automated VM provisioning

*VM catalog, IP automation and IPAM, DNS and firewall tasks in parallel.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![VM provisioning: current process](https://raphaelfcs.github.io/portfolio/artigos/img/provisionamento-de-vms-en-1.webp)

> **TL;DR:** A VM request that takes weeks is a process problem, not a technology one.

## Problem

Linux VM and database creation with many manual approvals.

## Solution

Catalog with standards, Python automation that finds a free IP, IPAM, DNS and firewall tasks in parallel and the VM created by Terraform. PaaS database by default.

### VM provisioning: current process

1. The request arrives in a spreadsheet with 20+ fields.
2. DNS ticket to define the hostname.
3. IP looked up by hand in Azure and IPAM.
4. Firewall rule and NAT through another queue.
5. An infrastructure war room creates the VM by script.
6. DBA installs the IaaS database and the SLA is missed.

> **Note:** Each queue waits for the previous one: weeks for a simple VM.

### VM provisioning: proposed process

1. Request starts from a standards catalog.
2. Automation validates hostname and finds a free IP.
3. IPAM, DNS and firewall run in parallel.
4. VM created by Terraform.
5. PaaS database by default; IaaS only when justified.

> **Note:** Catalog defaults: Standard disk in dev/hml and Premium in prd, no public IP, backup and monitoring on, mandatory tags.
> **Note:** The VM goes through the workload pipeline of the IaC monorepo pattern (padrao-iac).

![Figure 2: VM provisioning: proposed process](https://raphaelfcs.github.io/portfolio/artigos/img/provisionamento-de-vms-en-2.webp)
*Figure 2: VM provisioning: proposed process*

## The code

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

## Discussion

**Terraform modules used:** [azure/sql-database](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/sql-database), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| azure/sql-database | database vCores or DTUs | serverless for intermittent workloads and reservations for PRD |
| azure/monitor-alerts | alerts and Log Analytics ingestion | per-table retention and budget alerts (Cost Management) |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/provisionamento-de-vms/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
