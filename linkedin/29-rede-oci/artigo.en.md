# Hybrid network on OCI

*Firewall hub per region, FastConnect to two datacenters and remote peering for DR.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![Hybrid network on OCI: hub per region](https://raphaelfcs.github.io/portfolio/artigos/img/rede-oci-en-1.webp)

> **TL;DR:** Hybrid network on OCI: the drawing that unblocked the project.

## Problem

Systems on Oracle Cloud that needed to talk to the AWS platform and two datacenters.

## Solution

Firewall hub per region, FastConnect to both datacenters, DRGs and remote peering between regions. Mapping CIDRs in one drawing avoided overlaps and weeks of e-mails.

### Hybrid network on OCI: hub per region

1. Two datacenters reach each region over FastConnect.
2. DRG sends traffic to the firewall hub.
3. Hub routes to application VCNs.
4. Remote peering connects regions for DR.

> **Note:** /21 ranges per VCN planned with no overlap with AWS.

## Discussion

This is a process and governance diagram: the lab provides the step-by-step and references, with no automation of its own.

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| — | cross-cloud traffic and idle instances | cost tags and a monthly interconnect review |

The FinOps cycle I use (inform, optimize, operate) is drawn in the FinOps process lab in the repository.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/rede-oci/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
