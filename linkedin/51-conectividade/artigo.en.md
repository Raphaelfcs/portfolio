# Asynchronous queue integration on Azure

*API receives requests over ExpressRoute, a queue per app, Container Apps consumers and Cosmos DB.*

Raphael Santos · 3 min read · Azure governance and modernization for an insurer (2024-2025)

![Asynchronous integration with a queue per app](https://raphaelfcs.github.io/portfolio/artigos/img/conectividade-en-1.webp)

> **TL;DR:** Sixty applications, one pattern: a queue per app.

## Problem

Insurer integrating on-premises systems with Azure.

## Solution

Requests arrive over ExpressRoute, the API posts to a queue, Container Apps consumers process and write to Cosmos DB, and the answer goes back through a response queue.

### Asynchronous integration with a queue per app

1. On-premises system arrives over ExpressRoute.
2. API posts the request to the queue.
3. Container Apps consumers process it.
4. State stored in Cosmos DB.
5. Result goes to the response queue.
6. API returns the response to the caller.

> **Note:** Pattern replicated for 60 apps, one queue per app.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | subscriptions without an owner and idle VMs | tags by policy, Cost Management budgets and Advisor |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/seguradora/conectividade/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
