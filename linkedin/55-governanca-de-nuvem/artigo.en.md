# Cloud governance and migration sizing

*Migration timeline formula from servers, team and buffer, executed through IaC.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![Cloud governance and migration sizing](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-de-nuvem-en-1.webp)

> **TL;DR:** How many servers, how long, and how to govern afterwards?

## Problem

Azure migration program needing numbers and rules before starting.

## Solution

A timeline formula from servers, engineers and buffer (1,400 servers ≈ 14.5 months with 4 engineers) turned into a wave plan executed by IaC.

### Cloud governance and migration sizing

1. Server inventory.
2. Formula with a 13% buffer and 5 working days.
3. Timeline becomes a wave plan.
4. Waves executed via IaC on governed subscriptions.

### IaC on Azure with the three pipelines

1. Platform publishes engines by tag.
2. Boilerplate uses the engines and is tested.
3. Project starts from the boilerplate.
4. An approved PR triggers the pipeline.
5. Apply per subscription, with approval in prd and dr.

> **Note:** First resource in 1-2 weeks; next ones in 1-2 days and ~15 min per environment.
> **Note:** Full pattern, including GitLab and GitHub, in padrao-iac.

![Figure 2: IaC on Azure with the three pipelines](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-de-nuvem-en-2.webp)
*Figure 2: IaC on Azure with the three pipelines*

## The code

```hcl
module "storage_account" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//azure/storage-account"

  name                 = "stdemodev001"
  resource_group_name  = "rg-demo-dev"
  location             = "brazilsouth"
  cmk_key_vault_id     = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-demo-dev/providers/Microsoft.KeyVault/vaults/kv-demo-dev"
  cmk_key_vault_key_id = "https://kv-demo-dev.vault.azure.net/keys/storage"
  containers           = ["dados", "backup"]
  tags                 = local.tags
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

**Terraform modules used:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts), [azure/monitor-diagnostic-setting](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-diagnostic-setting)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| azure/storage-account | Storage capacity and transactions | Cool/Archive tiers through lifecycle policies |
| azure/monitor-alerts | alerts and Log Analytics ingestion | per-table retention and budget alerts (Cost Management) |
| azure/monitor-diagnostic-setting | diagnostic log ingestion | send only the needed categories and archive to Storage |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/governanca-de-nuvem/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
