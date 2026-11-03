# Processo de FinOps

*Ciclo informar, otimizar e operar, com responsáveis, cadência e guardrails.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Processo de FinOps: informar, otimizar, operar](https://raphaelfcs.github.io/portfolio/artigos/img/processo-finops-pt-1.webp)

> **Em resumo:** FinOps é ciclo: informar, otimizar e operar, toda semana.

## O problema

Conta de nuvem crescendo sem dono claro para cada custo.

## A solução

Ciclo com responsáveis e cadência, apoiado por export CUR/FOCUS, relatório de custo, conformidade de tags e scheduler de instâncias.

### Processo de FinOps: informar, otimizar, operar

1. Tags obrigatórias e export de custo alimentam o relatório.
2. KPIs por área e showback/chargeback.
3. Desvios viram recomendações priorizadas.
4. Time misto executa com os donos dos recursos.
5. O que se repete vira guardrail ou agenda automática.

## O código

```hcl
module "cur_focus_export" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/cur-focus-export"

  bucket_name    = "demo-finops-focus-123456789012"
  retention_days = 730
  tags           = local.tags
}

module "finops_cost_report" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/finops-cost-report"

  name_prefix         = local.name_prefix
  bucket_name         = "demo-finops-relatorios-123456789012"
  alert_topic_arn     = "arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"
  cost_allocation_tag = "CentroCusto"
  tags                = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/cur-focus-export](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cur-focus-export), [aws/finops-cost-report](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/finops-cost-report), [aws/tag-compliance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tag-compliance), [aws/instance-scheduler](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/instance-scheduler)

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
