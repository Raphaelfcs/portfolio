# Challenge: serverless API

*API Gateway + Lambda in a private subnet, all in Terraform.*

Raphael Santos · 3 min read · Architecture technical challenges

![Challenge: serverless API with IaC](https://raphaelfcs.github.io/portfolio/artigos/img/desafio-api-serverless-en-1.webp)

> **TL;DR:** Technical challenge: a serverless API with IaC from scratch.

## Problem

Interview challenge asking for a working, secure and reproducible API.

## Solution

API Gateway + Lambda in a private subnet, everything in Terraform. Easy to understand and to destroy at the end.

### Challenge: serverless API with IaC

1. User calls the route.
2. Gateway invokes Lambda.
3. Internet egress via NAT when needed.

## The code

```hcl
module "lambda_function" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/lambda-function"

  function_name       = "demo-dev-relatorio"
  source_dir          = "${path.module}/src"
  schedule_expression = "rate(1 day)"
  environment         = { NIVEL_LOG = "INFO" }
  tags                = local.tags
}

module "api_gateway_lambda" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/api-gateway-lambda"

  name                 = "demo-dev-api"
  lambda_function_name = module.lambda_function.function_name
  lambda_invoke_arn    = module.lambda_function.invoke_arn
  tags                 = local.tags
}
```

## Discussion

**Terraform modules used:** [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/api-gateway-lambda](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/api-gateway-lambda)

### FinOps: where the cost is

| Component | What drives cost | Lever |
|---|---|---|
| aws/lambda-function | function duration × memory | tune memory with Power Tuning and use arm64 |
| aws/api-gateway-lambda | API Gateway requests | HTTP API instead of REST API when the extra features are not needed, plus edge caching |

In the repository, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export and aws/instance-scheduler close the loop: mandatory tags, cost report, CUR/FOCUS export and shutdown schedule.

## See also

- [Full lab on GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/desafios/desafio-api-serverless/README.en.md)
- [FinOps process](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.en.md)
- [All articles](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos is a Lead Cloud Architect with 9+ years in DevOps and cloud architecture on AWS, Google Cloud and Azure. All the code in this article is on GitHub.*

*Company names, accounts and IDs were removed; values in the code are fictitious.*
