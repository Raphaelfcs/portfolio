# DR de file system no Azure

*Azure Files com File Sync, replicação GRS e failover entre regiões pelo F5.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![DR de file system no Azure](https://raphaelfcs.github.io/portfolio/artigos/img/dr-de-arquivos-azure-pt-1.webp)

> **Em resumo:** DR de file system: o que importa é o tempo de volta.

## O problema

Compartilhamento de arquivos crítico sem plano de recuperação.

## A solução

Replicação para outra região, RPO/RTO acordados e teste de failover documentado.

### DR de file system no Azure

1. F5 decide a região.
2. Região A atende em produção.
3. Arquivos em Azure Files com File Sync.
4. Replicação geográfica para a região B.
5. Failover pelo F5 quando a região A cai.

> **Nota:** ~90 TB; RPO/RTO acordados e custo de cada opção (LRS, ZRS, GRS) no desenho original.

## O código

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

## Discussão

**Módulos Terraform usados:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| azure/storage-account | capacidade e transações no Storage | tiers Cool/Archive por política de ciclo de vida |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/dr-de-arquivos-azure/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
