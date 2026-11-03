# Modernização de load balancers

*AS-IS do caminho de uma cotação, onde o tempo é gasto e o que muda no alvo.*

Raphael Santos · 3 min de leitura · Governança e modernização em Azure para uma seguradora (2024-2025)

![Modernização de load balancers: AS-IS](https://raphaelfcs.github.io/portfolio/artigos/img/modernizacao-de-load-balancers-pt-1.webp)

> **Em resumo:** Modernizar balanceador começa por entender o AS-IS.

## O problema

Balanceadores antigos com regras acumuladas ao longo dos anos.

## A solução

Três visões do AS-IS (balanceamento, infraestrutura e aplicação) antes de propor o alvo.

### Modernização de load balancers: AS-IS

1. Requisição chega pelo DNS e firewall.
2. Sessão sticky prende o usuário a um servidor.
3. Back-end responde em até 6 s; pior caso 13 s em pico.
4. Parceiros entram por uma camada de API.

> **Nota:** O alvo remove a sessão sticky e separa leitura e escrita para escalar horizontalmente.

## Discussão

Este desenho é de processo e governança: o lab traz o passo a passo e as referências, sem automação própria.

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | assinaturas sem dono e VMs ociosas | tags por política, orçamento no Cost Management e Advisor |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/modernizacao-de-load-balancers/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
