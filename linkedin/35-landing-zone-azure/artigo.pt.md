# Landing zone Azure com AKS privado

*Front Door, Private Link Service, AKS em três zonas e banco por Private Endpoint.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Landing zone Azure com AKS privado](https://raphaelfcs.github.io/portfolio/artigos/img/landing-zone-azure-pt-1.webp)

> **Em resumo:** Landing zone Azure dentro de uma governança multicloud.

## O problema

Azure entrando em uma empresa que já tinha governança na AWS.

## A solução

Management groups, assinaturas e rede alinhados aos mesmos princípios de contas e guardrails da AWS.

### Landing zone Azure com AKS privado

1. Entrada global pelo Front Door.
2. Origem privada via Private Link Service.
3. LB interno até o AKS em três zonas.
4. Banco acessado só por Private Endpoint.

## Discussão

Este desenho é de processo e governança: o lab traz o passo a passo e as referências, sem automação própria.

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | assinaturas sem dono e VMs ociosas | tags por política, orçamento no Cost Management e Advisor |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/landing-zone-azure/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
