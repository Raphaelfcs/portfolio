# FinOps: current and target process

*Assessment of the manual flow and a V1 proposal with automated collection and owner decisions.*

Raphael Santos · 3 min read · FinOps assessment and process (2024)

![FinOps: current process (AS-IS)](https://raphaelfcs.github.io/portfolio/artigos/img/finops-atual-x-alvo-en-1.webp)

> **TL;DR:** FinOps assessment: does the current process fit in one drawing?

## Problem

Client with a cost process based on spreadsheets and e-mails, validated only after the next invoice.

## Solution

I drew the AS-IS and the V1 proposal: automated collection, recommendations with estimated savings and a synchronous decision with the owners, escalating to CTO/CFO when needed.

### FinOps: current process (AS-IS)

1. Request enters the backlog.
2. Up to 4 days waiting.
3. Manual collection.
4. Recommendation in slides.
5. Result only confirmed on the next invoice.

### FinOps: V1 proposal

1. Request triggers automation.
2. Automatic collection and comparison.
3. Recommendation with estimated savings.
4. Synchronous decision with owners.
5. If not applied, escalate to CTO/CFO.

![Figure 2: FinOps: V1 proposal](https://raphaelfcs.github.io/portfolio/artigos/img/finops-atual-x-alvo-en-2.webp)
*Figure 2: FinOps: V1 proposal*

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

**Terraform modules used:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts)

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/finops/finops-atual-x-alvo/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
