# Governança de IaC e DevOps no Azure

*Engines versionadas, revisão obrigatória e Azure Pipelines com state por projeto.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Governança de IaC e DevOps no Azure](https://raphaelfcs.github.io/portfolio/artigos/img/governanca-iac-devops-pt-1.webp)

> **Em resumo:** Governança de IaC: ferramentas, pipeline, branches e diretórios no mesmo desenho.

## O problema

Times provisionando Azure manualmente e sem padrão de repositório.

## A solução

Uma página para cada camada: ferramentas, pipeline de IaC, estratégia de branches e estrutura de diretórios.

### Governança de IaC e DevOps no Azure

1. Workload consome engines por tag.
2. Revisão obrigatória no PR.
3. Pipeline executa init, validate e plan.
4. Apply por ambiente, state separado por projeto.

> **Nota:** Primeiro recurso em 1-2 semanas; os seguintes em 1-2 dias e ~15 min por ambiente.

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

module "monitor_diagnostic_setting" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//azure/monitor-diagnostic-setting"

  target_resource_ids        = ["/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-app/providers/Microsoft.KeyVault/vaults/kv-demo"]
  log_analytics_workspace_id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-monitoria/providers/Microsoft.OperationalInsights/workspaces/law-plataforma"
}
```

## Discussão

**Módulos Terraform usados:** [azure/storage-account](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/storage-account), [azure/monitor-diagnostic-setting](https://github.com/Raphaelfcs/automacao_terraform/tree/main/azure/monitor-diagnostic-setting)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| azure/storage-account | capacidade e transações no Storage | tiers Cool/Archive por política de ciclo de vida |
| azure/monitor-diagnostic-setting | ingestão de logs de diagnóstico | enviar só as categorias necessárias e arquivar no Storage |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/governanca-iac-devops/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
