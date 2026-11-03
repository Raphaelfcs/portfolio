# Cloud service portfolio

*From catalog request to a pipeline-delivered resource in ~15 minutes.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![Cloud service portfolio](https://raphaelfcs.github.io/portfolio/artigos/img/portfolio-de-servicos-en-1.webp)

> **TL;DR:** Cloud as a product: a service portfolio for business units.

## Problem

Business units asking for "cloud" without knowing what existed.

## Solution

A catalog with what is offered and for whom, workloads from a boilerplate and resources delivered by pipeline in about 15 minutes per environment.

### Cloud service portfolio

1. Business unit picks from the catalog.
2. Workload created from the boilerplate.
3. Pipeline validates and applies.
4. Resource delivered per environment.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | subscriptions without an owner and idle VMs | tags by policy, Cost Management budgets and Advisor |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/portfolio-de-servicos/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
