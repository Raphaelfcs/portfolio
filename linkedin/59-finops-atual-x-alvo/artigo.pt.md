# FinOps: processo atual e alvo

*Assessment do fluxo manual e proposta V1 com coleta automatizada e decisão com os donos.*

Raphael Santos · 3 min de leitura · Assessment e processo de FinOps (2024)

![FinOps: processo atual (AS-IS)](https://raphaelfcs.github.io/portfolio/artigos/img/finops-atual-x-alvo-pt-1.webp)

> **Em resumo:** Assessment de FinOps: o processo atual cabe em um desenho?

## O problema

Cliente com processo de custos baseado em planilhas e e-mails.

## A solução

Desenhei o AS-IS e a proposta V1: coleta automatizada, backlog de recomendações e aprovação pelos responsáveis.

### FinOps: processo atual (AS-IS)

1. Pedido entra no backlog.
2. Espera de até 4 dias.
3. Coleta manual.
4. Recomendação em apresentação.
5. Resultado só confirmado na fatura seguinte.

### FinOps: proposta V1

1. Pedido dispara a automação.
2. Coleta e comparação automáticas.
3. Recomendação já com ganho estimado.
4. Decisão síncrona com os donos.
5. Sem aplicação, sobe para CTO/CFO.

![Figura 2: FinOps: proposta V1](https://raphaelfcs.github.io/portfolio/artigos/img/finops-atual-x-alvo-pt-2.webp)
*Figura 2: FinOps: proposta V1*

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

**Módulos Terraform usados:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts)

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/finops/finops-atual-x-alvo/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
