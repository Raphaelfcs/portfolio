# MVP de automação de processos com IA

*MVP que recebe documentos, extrai dados com IA gerenciada e devolve o resultado para o sistema de origem com rastreabilidade.*

Raphael Santos · 3 min de leitura · Estudos de caso de arquitetura (2026)

![Case 2 — Arquitetura do MVP](https://raphaelfcs.github.io/portfolio/artigos/img/automacao-com-ia-mvp-pt-1.webp)

> **Em resumo:** Um MVP de IA não precisa de um cluster de GPU. Precisa de rastreabilidade.

## O problema

Processo manual de leitura de documentos, com retrabalho e sem trilha de quem fez o quê.

## A solução

Textract + filas + barramento de eventos resolvem 80% do problema com serviços gerenciados; o que torna o MVP confiável é cada documento ter estado, dono e histórico.

## O código

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
}

module "textract_pipeline" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/textract-pipeline"

  name_prefix = "demo-dev-ocr"
  kms_key_arn = module.kms_key.key_arn
  tags        = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/textract-pipeline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/textract-pipeline), [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/cognito-user-pool](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cognito-user-pool), [aws/cloudfront-spa](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/cloudfront-spa)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/textract-pipeline | custo por página processada no Textract | filtrar e classificar antes de extrair e usar só as features necessárias (texto x formulário x tabela) |
| aws/cloudfront-spa | transferência de dados da CDN | cache bem configurado e compressão; a CDN costuma reduzir o custo de saída da origem |
| aws/cognito-user-pool | usuários ativos por mês (MAU) no Cognito | escolher o tier certo e limpar contas inativas |
| aws/kms-key | chaves KMS por mês e chamadas de API | bucket keys no S3 reduzem chamadas ao KMS |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/estudos-de-caso/automacao-com-ia-mvp/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
