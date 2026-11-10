# IAM Identity Center as code: access with no IAM users

*Groups, permission sets and assignments versioned in Terraform, with a separate break-glass and pipelines over OIDC.*

Raphael Santos · 3 min read · Hands-on AWS

![aws/identity-center-permission-set: IAM Identity Center: permission sets and assignments](https://raphaelfcs.github.io/portfolio/artigos/img/aws-identity-center-en-1.webp)

> **TL;DR:** In a multi-account environment, every IAM user is a long-lived key waiting to leak. Human access lives in IAM Identity Center, and pipeline access in OIDC.

## Problem

The typical scenario: dozens of accounts, IAM users created account by account, old access keys and nobody knowing who can reach what. Audits turn into spreadsheets, and offboarding someone takes days.

## Solution

Groups in the Identity Center directory (or synced from the corporate IdP), permission sets with managed, inline and customer managed policies and a permissions boundary, and group-to-account assignments, all in Terraform. Reviewing access becomes reviewing a pull request. IAM users remain only for break-glass and legacy integrations, and pipelines assume roles over OIDC, with no long-lived keys.

### How to build it

1. Define groups by role, not by person: platform admins, developers, read-only, FinOps.
2. Create permission sets with least privilege and a short session duration for the write ones.
3. Assign group to account based on OU and environment: write in dev, read in prd.
4. Use a delegated administrator so Identity Center is not operated from the management account.
5. Keep an IAM break-glass group with mandatory MFA, outside Identity Center.
6. Replace pipeline keys with roles assumed over OIDC, one for plan and one for deploy with approval.

> **Note:** A permission set change is reprovisioned in every assigned account. Test it in a sandbox account first.

![Figure 2: aws/identity-center-groups: IAM Identity Center: groups and users](https://raphaelfcs.github.io/portfolio/artigos/img/aws-identity-center-en-2.webp)
*Figure 2: aws/identity-center-groups: IAM Identity Center: groups and users*

## The code

```hcl
module "identity_center_permission_set" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/identity-center-permission-set?ref=main"

  permission_sets = {
    RedeLeitura = { description = "Rede somente leitura", managed_policy_arns = ["arn:aws:iam::aws:policy/job-function/ViewOnlyAccess"], inline_policy = file("${path.module}/politicas/rede-leitura.json") }
    Deploy      = { description = "Deploy de aplicacoes", session_duration = "PT2H", managed_policy_arns = ["arn:aws:iam::aws:policy/PowerUserAccess"] }
  }
  account_assignments = [
    { permission_set = "RedeLeitura", group = "time-rede", account_id = "123456789012" },
    { permission_set = "Deploy", group = "time-apps", account_id = "123456789012" },
  ]
  tags = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/identity-center-groups](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/identity-center-groups), [aws/identity-center-permission-set](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/identity-center-permission-set), [aws/iam-group](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-group), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/identity-center-permission-set | Nothing: Identity Center has no per-user charge. | Less operational time spent on access requests and audits. |
| aws/iam-github-oidc | Nothing: OIDC is free. | Removes key rotation and the risk of leaks. |

Values vary with region and volume; the table shows where to look first.

## See also

- [Main module on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/identity-center-groups/README.en.md)
- [Hands-on AWS map in the monorepo](https://github.com/Raphaelfcs/automacao_terraform/blob/main/README.en.md#hands-on-aws-experience-where-it-lives-in-the-code)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
