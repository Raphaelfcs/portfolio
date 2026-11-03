# File system DR on Azure

*Azure Files with File Sync, GRS replication and cross-region failover via F5.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![File system DR on Azure](https://raphaelfcs.github.io/portfolio/artigos/img/dr-de-arquivos-azure-en-1.webp)

> **TL;DR:** File system DR: what matters is the time to come back.

## Problem

Critical file share with no recovery plan.

## Solution

Azure Files with File Sync, GRS replication to a second region and failover driven by the on-premises F5, with RPO/RTO and cost per option agreed upfront.

### File system DR on Azure

1. F5 picks the region.
2. Region A serves production.
3. Files on Azure Files with File Sync.
4. Geo-replication to region B.
5. F5 fails over when region A is down.

> **Note:** ~90 TB; agreed RPO/RTO and cost per option (LRS, ZRS, GRS) in the original drawing.

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
```

## Discussion

**Terraform modules used:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| azure/storage-account | Storage capacity and transactions | Cool/Archive tiers through lifecycle policies |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/dr-de-arquivos-azure/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
