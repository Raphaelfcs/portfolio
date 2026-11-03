# B2C authentication — first version

*First version on EKS with IRSA, Secrets Manager and a database per service.*

Raphael Santos · 3 min read · AWS platform of a health insurer (2024)

![B2C authentication — first version on EKS](https://raphaelfcs.github.io/portfolio/artigos/img/autenticacao-b2c-v1-en-1.webp)

> **TL;DR:** The first version of a service says a lot about the second.

## Problem

First version of the B2C authentication service.

## Solution

On EKS with IRSA, credentials in Secrets Manager and a database owned by the service. The Fargate version came later with the volume.

### B2C authentication — first version on EKS

1. App calls the API.
2. Gateway forwards to the EKS service.
3. Pod assumes its role through IRSA.
4. Database credential comes from Secrets Manager.
5. The service owns its data.

## The code

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "cognito_user_pool" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/cognito-user-pool"

  name_prefix       = local.name_prefix
  domain_prefix     = "demo-dev-login"
  callback_urls     = ["https://app.example.com/callback"]
  logout_urls       = ["https://app.example.com/"]
  custom_attributes = { tenant_id = 64 }
  roles             = { admin = "Administradores", operador = "Operacao" }
  machine_scopes    = { "pedidos.read" = "Ler pedidos", "pedidos.write" = "Gravar pedidos" }
  service_clients   = { faturamento = ["pedidos.read"] }
  tags              = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/cognito-user-pool | Cognito monthly active users (MAU) | pick the right tier and clean up inactive accounts |
| aws/kms-key | KMS keys per month and API calls | S3 bucket keys reduce KMS calls |
| aws/api-gateway-lambda | API Gateway requests | HTTP API instead of REST API when the extra features are not needed, plus edge caching |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/saude/autenticacao-b2c-v1/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
