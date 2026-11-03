# AWS fundamentals: identity and guardrails

*Training material: Identity Center, OUs, SCPs, boundaries and resource policies.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![AWS fundamentals: identity and guardrails](https://raphaelfcs.github.io/portfolio/artigos/img/fundamentos-aws-en-1.webp)

> **TL;DR:** Training material is architecture too.

## Problem

New team needing a common AWS foundation.

## Solution

Federated access with MFA, permission sets, SCPs as the ceiling of each OU, permission boundaries and resource policies, drawn with the same icons used in real projects.

### AWS fundamentals: identity and guardrails

1. Federated human access with MFA, no IAM users.
2. Permission sets per account.
3. SCP sets the ceiling of each OU.
4. Boundary limits what a role can delegate.
5. Resource policy locks access at the resource.

> **Note:** Least privilege always; root protected with MFA and never used daily.

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

module "iam_group" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/iam-group"

  name                = "break-glass"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
  require_mfa         = true
}
```

## Discussion

**Terraform modules used:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/iam-group](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-group), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/s3-bucket](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/s3-bucket)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |
| aws/s3-bucket | S3 storage and old object versions | lifecycle to IA/Glacier and expiration of noncurrent versions |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/fundamentos-aws/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
