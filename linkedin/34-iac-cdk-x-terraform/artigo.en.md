# IaC: CDK vs Terraform

*The same trunk-based flow in CDK and Terraform, from engine to workload.*

Raphael Santos · 3 min read · CCoE, landing zone and platform of a telecom operator (2025-2026)

![IaC: the same flow in CDK and Terraform](https://raphaelfcs.github.io/portfolio/artigos/img/iac-cdk-x-terraform-en-1.webp)

> **TL;DR:** CDK or Terraform? I built the same flow in both.

## Problem

Recurring team discussion about which IaC tool to adopt.

## Solution

Same trunk-based flow in both tools, side by side, with delivery in about 15 minutes per environment. The choice became about the team and the ecosystem, not taste.

### IaC: the same flow in CDK and Terraform

1. Team starts from the boilerplate and commits.
2. Mandatory review.
3. Pipeline validates and builds the plan.
4. Plan (Terraform) or synth (CDK).
5. Delivery in ~15 minutes per environment.

## The code

```hcl
module "tf_backend_bootstrap" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tf-backend-bootstrap"

  bucket_name = "demo-tfstate-123456789012"
  tags        = local.tags
}

module "vpc" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/vpc"

  name_prefix        = local.name_prefix
  cidr_block         = "10.20.0.0/16"
  azs                = ["sa-east-1a", "sa-east-1b"]
  single_nat_gateway = true
  eks_cluster_name   = "demo-dev"
  tags               = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/tf-backend-bootstrap](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tf-backend-bootstrap), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/vpc | NAT Gateway per AZ and the traffic it processes | a single NAT in DEV and VPC endpoints for S3/ECR to keep traffic off the NAT |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/iac-cdk-x-terraform/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
