# Moving a workload between AWS accounts

*Topology, identity dependency and findings that drive the organization move.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![Moving a workload between AWS accounts](https://raphaelfcs.github.io/portfolio/artigos/img/migracao-de-conta-aws-en-1.webp)

> **TL;DR:** Moving a workload between AWS accounts: topology, costs and findings.

## Problem

Workload running outside the company organization.

## Solution

A read-only scan showed all human access depended on one Identity Center. Create break-glass access first, then move into the organization with SCPs and the shared network.

### Moving a workload between AWS accounts

1. Today all human access depends on the current organization Identity Center.
2. In the company organization, SCPs and guardrails already exist.
3. The VPC moves onto the shared network.

> **Note:** Leaving the organization without a break-glass user locks the account: create it first.
> **Note:** Nothing outside sa-east-1, no Route 53 and no ACM: less to move.

## The code

```hcl
module "organizations_scp" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/organizations-scp"

  allowed_regions        = ["sa-east-1", "us-east-1"]
  required_tags          = ["CentroCusto", "Ambiente", "Dono"]
  create_tag_enforcement = ["CentroCusto"]
  attach_target          = ["Workloads", "Sandbox"]
  tags                   = local.tags
}

module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/transit-gateway-attachment | Transit Gateway attachments and processed GB | consolidate attachments and keep high-volume traffic off the TGW |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/migracao-de-conta-aws/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
