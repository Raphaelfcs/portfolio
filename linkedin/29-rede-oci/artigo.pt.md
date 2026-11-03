# Rede híbrida na OCI

*Hub com firewalls por região, FastConnect a dois datacenters e peering remoto para DR.*

Raphael Santos · 3 min de leitura · Plataforma AWS de uma operadora de saúde (2024)

![Rede híbrida na OCI: hub por região](https://raphaelfcs.github.io/portfolio/artigos/img/rede-oci-pt-1.webp)

> **Em resumo:** Rede híbrida AWS + OCI: o desenho que destravou o projeto.

## O problema

Sistemas na Oracle Cloud precisando falar com a plataforma na AWS.

## A solução

Mapear CIDRs, rotas e pontos de conexão em um único desenho evitou sobreposição de faixas e semanas de troca de e-mails.

### Rede híbrida na OCI: hub por região

1. Dois datacenters chegam por FastConnect em cada região.
2. DRG envia o tráfego ao hub com firewalls.
3. Hub distribui para as VCNs de aplicação.
4. Peering remoto liga as regiões para DR.

> **Nota:** Faixas /21 por VCN planejadas sem sobreposição com a AWS.

## Discussão

Este desenho é de processo e governança: o lab traz o passo a passo e as referências, sem automação própria.

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| — | tráfego entre nuvens e instâncias ociosas | tags de custo e revisão mensal de interconexão |

O ciclo de FinOps (informar, otimizar, operar) que uso está desenhado no lab de Processo de FinOps do repositório.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/rede-oci/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
