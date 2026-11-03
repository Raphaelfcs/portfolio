# Azure landing zone with private AKS

*Front Door, Private Link Service, AKS across three zones and a database through Private Endpoint.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![Azure landing zone with private AKS](https://raphaelfcs.github.io/portfolio/artigos/img/landing-zone-azure-en-1.webp)

> **TL;DR:** Azure landing zone with private AKS: nothing public behind Front Door.

## Problem

Azure joining a company that already had AWS governance.

## Solution

Front Door as the global entry, Private Link Service to the internal LB, AKS across three zones and the database only through Private Endpoint.

### Azure landing zone with private AKS

1. Global entry through Front Door.
2. Private origin through Private Link Service.
3. Internal LB to AKS across three zones.
4. Database reached only through Private Endpoint.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | subscriptions without an owner and idle VMs | tags by policy, Cost Management budgets and Advisor |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/landing-zone-azure/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
