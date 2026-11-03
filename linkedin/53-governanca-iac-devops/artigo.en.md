# IaC and DevOps governance on Azure

*Versioned engines, mandatory review and Azure Pipelines with state per project.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![IaC and DevOps governance on Azure](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-iac-devops-en-1.webp)

> **TL;DR:** IaC governance: engines, review, pipeline and state in one drawing.

## Problem

Teams provisioning Azure by hand with no repository standard.

## Solution

Workloads consume versioned engines by tag, PRs are reviewed, Azure Pipelines runs init, validate and plan, and state is split per project.

### IaC and DevOps governance on Azure

1. Workload consumes engines by tag.
2. Mandatory PR review.
3. Pipeline runs init, validate and plan.
4. Apply per environment, state split per project.

> **Note:** First resource in 1-2 weeks; next ones in 1-2 days and ~15 min per environment.

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

module "monitor_diagnostic_setting" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//azure/monitor-diagnostic-setting"

  target_resource_ids        = ["/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-app/providers/Microsoft.KeyVault/vaults/kv-demo"]
  log_analytics_workspace_id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-monitoria/providers/Microsoft.OperationalInsights/workspaces/law-plataforma"
}
```

## Discussion

**Terraform modules used:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-diagnostic-setting](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-diagnostic-setting)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| azure/storage-account | Storage capacity and transactions | Cool/Archive tiers through lifecycle policies |
| azure/monitor-diagnostic-setting | diagnostic log ingestion | send only the needed categories and archive to Storage |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/governanca-iac-devops/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
