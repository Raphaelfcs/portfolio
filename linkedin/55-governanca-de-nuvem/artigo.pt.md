# Governança de nuvem e cálculo de migração

*Fórmula de prazo de migração a partir de servidores, time e buffer, executada por IaC.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Governança de nuvem e cálculo de migração](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-de-nuvem-pt-1.webp)

> **Em resumo:** Quantos servidores migrar, quanto custa e como governar depois?

## O problema

Programa de migração para Azure precisando de números e regras antes de começar.

## A solução

Cálculo de migração de servidores, IaC, pipeline e estrutura de diretórios: governança desenhada antes do primeiro recurso.

### Governança de nuvem e cálculo de migração

1. Inventário de servidores.
2. Fórmula com buffer de 13% e 5 dias úteis.
3. Prazo vira plano de ondas.
4. Ondas executadas por IaC sobre assinaturas governadas.

### IaC no Azure com as três esteiras

1. Plataforma publica engines por tag.
2. Boilerplate usa as engines e é testado.
3. Projeto nasce do boilerplate.
4. PR aprovado dispara o pipeline.
5. Apply por assinatura, com aprovação em prd e dr.

> **Nota:** Primeiro recurso em 1-2 semanas; os seguintes em 1-2 dias e ~15 min por ambiente.
> **Nota:** Padrão completo, com GitLab e GitHub, em padrao-iac.

![Figura 2: IaC no Azure com as três esteiras](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-de-nuvem-pt-2.webp)
*Figura 2: IaC no Azure com as três esteiras*

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

**Módulos Terraform usados:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-alerts](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-alerts), [azure/monitor-diagnostic-setting](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-diagnostic-setting)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| azure/storage-account | capacidade e transações no Storage | tiers Cool/Archive por política de ciclo de vida |
| azure/monitor-alerts | alertas e ingestão no Log Analytics | retenção por tabela e alertas de orçamento (Cost Management) |
| azure/monitor-diagnostic-setting | ingestão de logs de diagnóstico | enviar só as categorias necessárias e arquivar no Storage |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/governanca-de-nuvem/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
