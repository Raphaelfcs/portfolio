# Load balancer modernization

*AS-IS path of a quote request, where time is spent and what changes in the target.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![Load balancer modernization: AS-IS](https://raphaelfcs.github.io/portfolio/artigos/img/modernizacao-de-load-balancers-en-1.webp)

> **TL;DR:** Modernizing load balancers starts with understanding the AS-IS.

## Problem

Old load balancers with rules accumulated over years and quotes taking up to 13 seconds.

## Solution

I drew the path of a quote and where the time goes. The target removes sticky sessions and splits reads and writes to scale out.

### Load balancer modernization: AS-IS

1. Request arrives through DNS and firewall.
2. Sticky session pins the user to one server.
3. Back-end answers in up to 6 s; worst case 13 s at peak.
4. Partners come in through an API layer.

> **Note:** The target removes sticky sessions and splits reads and writes to scale out.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | subscriptions without an owner and idle VMs | tags by policy, Cost Management budgets and Advisor |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/modernizacao-de-load-balancers/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
