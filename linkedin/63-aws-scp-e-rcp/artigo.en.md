# SCP and RCP: the data perimeter of an AWS organization

*One limits what your identities can do; the other, who can reach your resources. How I use both in multi-account landing zones.*

Raphael Santos · 4 min read · Hands-on AWS

![aws/organizations-scp: Organizations: OUs, SCPs, RCPs and Tag Policy](https://raphaelfcs.github.io/portfolio/artigos/img/aws-scp-e-rcp-en-1.webp)

> **TL;DR:** An SCP alone does not stop an outside account from reading your bucket. An RCP alone does not stop someone inside from turning off CloudTrail. A data perimeter needs both.

## Problem

In multi-account landing zones, the most common risk is not a sophisticated attack: it is a bucket policy opened by mistake, a role trusting a forgotten vendor account, a team creating resources in a region that is not allowed. SCPs cover the organization’s identities, but they do not reach anyone outside it.

## Solution

SCPs sit on the OUs: allowed regions, protection of CloudTrail, GuardDuty, Config and Security Hub, root denied, mandatory encryption and tags on create. RCPs, released by AWS at the end of 2024, close the other side: S3, STS, KMS, SQS and Secrets Manager only accept identities from the organization, AWS services and declared trusted accounts, always over TLS. A blown budget applies a freeze SCP. All of it in Terraform, with tests that check the policy content.

### How to build it

1. Design the OUs before the policies: Security, Infrastructure, Workloads (Prod and NonProd), Sandbox and Suspended.
2. Attach the protection SCPs to the OUs and exempt only the Control Tower, AFT and break-glass roles.
3. Enable the RESOURCE_CONTROL_POLICY type on the root and attach the RCPs to a sandbox OU first.
4. Declare the outside accounts that really need access (partner, backup) in rcp_trusted_accounts; everything else is denied.
5. Turn on budget-guardrail: when the ceiling is hit, an SCP denies creating or starting expensive resources until someone reviews it.

> **Note:** SCPs and RCPs do not apply to the management account. That is why it runs no workloads.

![Figure 2: aws/budget-guardrail: FinOps: cost cap with SCP freeze](https://raphaelfcs.github.io/portfolio/artigos/img/aws-scp-e-rcp-en-2.webp)
*Figure 2: aws/budget-guardrail: FinOps: cost cap with SCP freeze*

## The code

```hcl
module "organizations_scp" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/organizations-scp?ref=main"

  allowed_regions        = ["sa-east-1", "us-east-1"]
  required_tags          = ["CentroCusto", "Ambiente", "Dono"]
  create_tag_enforcement = ["CentroCusto"]
  attach_target          = ["Workloads", "Sandbox"]
  enable_rcp             = true
  tags                   = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/budget-guardrail](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/budget-guardrail), [aws/control-tower-ou-registration](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/control-tower-ou-registration)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/organizations-scp | Nothing: SCPs, RCPs and Tag Policies are free. | The Tag Policy standardizes CostCenter and Owner, the base of cost per team. |
| aws/budget-guardrail | Spend that only shows up on next month’s bill. | Forecast-based alerts and an automatic freeze through an SCP. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/organizations-scp/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
