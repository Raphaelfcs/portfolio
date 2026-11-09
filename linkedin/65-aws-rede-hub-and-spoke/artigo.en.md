# Hub-and-spoke AWS networking: VPC, Transit Gateway, VPN and Direct Connect

*A Network account, routes segmented by environment and hybrid connectivity with a backup path, all as code.*

Raphael Santos · 4 min read · Hands-on AWS

![aws/network-hub: Hub-and-spoke Network account](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-en-1.webp)

> **TL;DR:** VPC peering works until the tenth account. After that, the network needs a hub, segmented routes and someone who owns the addressing plan.

## Problem

With many accounts, peering becomes a mesh nobody can audit, CIDRs overlap and production traffic starts seeing development. The link to the data center or to partners lives in each VPC, each with its own VPN.

## Solution

A Network account holds the Transit Gateway, shared through RAM with the organization. Route tables separate prod, nonprod and shared: each spoke VPC is associated with its domain and only propagates where it should. Hybrid connectivity comes in through the hub, with Direct Connect over a transit VIF and a Site-to-Site VPN with BGP as the backup path. Inside the VPCs, three tiers per AZ, the data tier with no internet route, and VPC endpoints to reach AWS services without going through NAT.

### How to build it

1. Plan the addressing (IPAM) before the first attachment: a duplicated CIDR on the same TGW makes the destination unpredictable.
2. Create the Network account and share the Transit Gateway through RAM with the organization.
3. Separate route tables by domain: prod, nonprod and shared, with explicit association and propagation.
4. Attach each spoke VPC and add routes to the remote CIDRs through the TGW in its private route tables.
5. Bring up Direct Connect over a transit VIF and the VPN with BGP as the backup path.
6. Use VPC endpoints for ECR, STS, logs and SSM, and a gateway endpoint for S3, to cut NAT traffic.

> **Note:** I integrated a partner’s network with the same model: a dedicated attachment, in its own route table, with no view of the other VPCs.

![Figure 2: aws/vpc: Three-tier VPC](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-en-2.webp)
*Figure 2: aws/vpc: Three-tier VPC*

![Figure 3: aws/vpn-site-to-site: Declarative Site-to-Site VPN (TGW/VGW)](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-en-3.webp)
*Figure 3: aws/vpn-site-to-site: Declarative Site-to-Site VPN (TGW/VGW)*

## The code

```hcl
module "vpn_site_to_site" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/vpn-site-to-site?ref=main"

  transit_gateway_route_table_id = "tgw-rtb-0123456789abcdef0"
  vpn_connections = {
    matriz = {
      target_gateway_type = "transit_gateway"
      transit_gateway_id  = "tgw-0123456789abcdef0"
      routing_option      = "dynamic"
      customer_gateway    = { mode = "new", bgp_asn = 65010, ip_address = "203.0.113.10" }
    }
  }
  tags = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/network-hub](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/network-hub), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/vpn-site-to-site](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpn-site-to-site), [aws/vpc-endpoints](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc-endpoints)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/network-hub | Hourly charge per TGW attachment and per GB processed. | Consolidate small VPCs and avoid traffic between environments that does not need to exist. |
| aws/vpc-endpoints | NAT Gateway charging per GB to reach AWS services. | S3 gateway endpoint (free) and interface endpoints only for high-volume services. |
| aws/vpn-site-to-site | Hourly charge per VPN connection. | VPN as Direct Connect backup, not as the main path. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/network-hub/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
