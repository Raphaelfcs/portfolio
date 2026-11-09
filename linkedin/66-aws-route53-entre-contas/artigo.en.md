# Route 53 across accounts: private DNS, hybrid DNS and subdomain delegation

*Stable names for internal services, Resolver for on-premises and one public zone per account, with no lifecycle coupling between them.*

Raphael Santos · 4 min read · Hands-on AWS

![aws/route53-private-zone: Multi-account private Route 53 zone](https://raphaelfcs.github.io/portfolio/artigos/img/aws-route53-entre-contas-en-1.webp)

> **TL;DR:** A database address pasted into an environment variable is an incident waiting for the next instance replacement. A stable name in private DNS fixes it, and Route 53 handles the rest across accounts.

## Problem

In a multi-account environment, every team creates its own zone, nobody can resolve anyone else’s names, the data center sees nothing in AWS, and the company’s public zone becomes a file only one person knows how to edit.

## Solution

Private zones with stable names for databases, caches, ALBs and fixed-IP services, associated with the account’s VPCs and authorized for VPCs in other accounts. Route 53 Resolver, in the Network account, provides hybrid DNS with on-premises and other clouds through inbound and outbound endpoints and rules shared through RAM. Each account has its own public zone (dev.example.com in the dev account), with a wildcard ACM certificate and CAA, and the delegation to the parent zone lives in a separate state.

### How to build it

1. Create the private zone in the account that owns the service and associate it with local VPCs.
2. Authorize the association for VPCs in other accounts (or partners) and associate it from their side.
3. In the Network account, bring up the Resolver endpoints and share the forwarding rules through RAM.
4. Create one public zone per account and environment, with a DNS-validated wildcard ACM certificate and a CAA record.
5. Create the subdomain NS delegation in the parent zone in its own state, consuming the name servers as an output.

> **Note:** Keeping the delegation in a separate state means destroying the dev zone never requires touching the production state.

![Figure 2: aws/route53-zone-delegation: Route 53: cross-account subdomain delegation](https://raphaelfcs.github.io/portfolio/artigos/img/aws-route53-entre-contas-en-2.webp)
*Figure 2: aws/route53-zone-delegation: Route 53: cross-account subdomain delegation*

## The code

```hcl
module "route53_private_zone" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/route53-private-zone?ref=main"

  zone_name          = "interno.demo.local"
  vpcs               = { principal = { vpc_id = "vpc-0123456789abcdef0", region = "sa-east-1" } }
  cross_account_vpcs = { parceiro = { vpc_id = "vpc-0fedcba9876543210", region = "us-east-1" } }
  cname_records      = { db = "demo.abc123.sa-east-1.rds.amazonaws.com", api = "internal-api-123.sa-east-1.elb.amazonaws.com" }
  a_records          = { gateway = ["10.20.10.10", "10.20.11.10"] }
  tags               = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/route53-private-zone](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-private-zone), [aws/route53-public-zone](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-public-zone), [aws/route53-zone-delegation](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-zone-delegation), [aws/network-hub](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/network-hub)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/route53-private-zone | Monthly charge per hosted zone and per million queries. | One zone per service domain, not one per application. |
| aws/network-hub | Hourly charge per Resolver endpoint ENI. | Endpoints centralized in the Network account, shared through RAM, instead of a pair per VPC. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/route53-private-zone/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
