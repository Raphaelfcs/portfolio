# Storage legado: inventário antes da migração

*Mapeamento de processos e consumidores do storage antes de escolher o destino.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Storage legado: inventário antes da migração](https://raphaelfcs.github.io/portfolio/artigos/img/storage-legado-pt-1.webp)

> **Em resumo:** O storage legado é o primeiro inventário de qualquer migração.

## O problema

Storage corporativo antigo sustentando aplicações críticas.

## A solução

Documentar volumes, consumidores e dependências antes de escolher o destino na nuvem.

### Storage legado: inventário antes da migração

1. Levantar cada processo que toca o storage.
2. Mapear serviços consumidores e volumes.
3. Só então escolher o destino.

## Discussão

Este desenho é de processo e governança: o lab traz o passo a passo e as referências, sem automação própria.

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | assinaturas sem dono e VMs ociosas | tags por política, orçamento no Cost Management e Advisor |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/storage-legado/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
