# Legacy storage: inventory before migration

*Mapping storage processes and consumers before choosing the target.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![Legacy storage: inventory before migration](https://raphaelfcs.github.io/portfolio/artigos/img/storage-legado-en-1.webp)

> **TL;DR:** Legacy storage is the first inventory of any migration.

## Problem

Old corporate storage holding critical applications.

## Solution

List every process that reads and writes it, map consumers and volumes, and only then choose the target in the cloud.

### Legacy storage: inventory before migration

1. List every process that touches the storage.
2. Map consuming services and volumes.
3. Only then choose the target.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | subscriptions without an owner and idle VMs | tags by policy, Cost Management budgets and Advisor |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/storage-legado/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
