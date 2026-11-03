# Integração assíncrona com filas no Azure

*API recebe pedidos por ExpressRoute, fila por aplicação, consumidores em Container Apps e Cosmos DB.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Integração assíncrona com filas por aplicação](https://raphaelfcs.github.io/portfolio/artigos/img/conectividade-pt-1.webp)

> **Em resumo:** Antes de migrar, desenhe como tudo conversa hoje.

## O problema

Seguradora com ambientes espalhados e pouca documentação de conectividade.

## A solução

O desenho de conectividade virou a base do plano de migração e da negociação com fornecedores de rede.

### Integração assíncrona com filas por aplicação

1. Sistema on-premises chega por ExpressRoute.
2. API publica o pedido na fila.
3. Consumidores em Container Apps processam.
4. Estado gravado no Cosmos DB.
5. Resultado vai para a fila de resposta.
6. API devolve a resposta ao chamador.

> **Nota:** Padrão replicado para 60 aplicações, uma fila por aplicação.

## Discussão

Este desenho é de processo e governança: o lab traz o passo a passo e as referências, sem automação própria.

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | assinaturas sem dono e VMs ociosas | tags por política, orçamento no Cost Management e Advisor |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/conectividade/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
