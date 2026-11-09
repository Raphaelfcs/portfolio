# Automações de governança na AWS orientadas a eventos

*Tags, MFA, inventário IAM, certificados, achados de segurança e custo: o que eu automatizo com CloudTrail, EventBridge e Lambda.*

Raphael Santos · 4 min de leitura · AWS na prática

![aws/tag-compliance: Conformidade de tags por evento](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-pt-1.webp)

> **Em resumo:** Governança que depende de alguém lembrar de olhar uma tela não acontece. Ela precisa reagir ao evento no momento em que ele acontece.

## O problema

Comecei em 2017 com scripts boto3 rodando em cron: autotag de EC2, parar RDS sem tag, conferir MFA, listar certificados vencendo. Funcionavam, mas tinham credencial fixa, destinatário de e-mail no código e nenhum log com retenção.

## A solução

Redesenhei cada automação como módulo Terraform orientado a eventos. A criação de recurso registrada no CloudTrail chega ao EventBridge e dispara a Lambda de conformidade de tags. Uma regra gerenciada do Config confere MFA continuamente, e uma Lambda semanal manda o relatório. O inventário IAM sai semanalmente em JSON versionado no S3. Certificados avisam pelo evento nativo do ACM, sem código. Achados de GuardDuty e Security Hub chegam ao SNS por EventBridge. EC2 e RDS ligam e desligam por tag com o EventBridge Scheduler, e um relatório diário de custo sai do Cost Explorer.

### O que cada automação faz

1. tag-compliance: CloudTrail → EventBridge → Lambda aplica e valida tags na criação e alerta pelo SNS.
2. iam-mfa-audit: regra do Config contínua e Lambda semanal com usuários de console sem MFA.
3. iam-inventory-export: usuários, grupos, roles e políticas em JSON no S3 versionado e cifrado.
4. acm-expiry-alert: o evento de expiração do próprio ACM vira alerta, sem Lambda varrendo certificados.
5. security-baseline: achados de GuardDuty, Security Hub, Inspector e Macie por EventBridge → SNS.
6. instance-scheduler e finops-cost-report: liga e desliga por tag com fuso horário, e o custo do dia no SNS.

> **Nota:** Cada Lambda tem role própria de menor privilégio, log group com retenção e KMS, e alarme de erro. Nada de credencial fixa.

![Figura 2: aws/iam-mfa-audit: Auditoria de MFA](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-pt-2.webp)
*Figura 2: aws/iam-mfa-audit: Auditoria de MFA*

![Figura 3: aws/instance-scheduler: Agendador FinOps de EC2/RDS](https://raphaelfcs.github.io/portfolio/artigos/img/aws-automacoes-de-governanca-pt-3.webp)
*Figura 3: aws/instance-scheduler: Agendador FinOps de EC2/RDS*

## O código

```hcl
module "tag_compliance" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/tag-compliance?ref=main"

  name_prefix     = local.name_prefix
  required_tags   = ["CentroCusto", "Ambiente", "Dono"]
  alert_topic_arn = "arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"
  tags            = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/tag-compliance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/tag-compliance), [aws/iam-mfa-audit](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-mfa-audit), [aws/iam-inventory-export](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-inventory-export), [aws/acm-expiry-alert](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/acm-expiry-alert), [aws/security-baseline](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/security-baseline), [aws/instance-scheduler](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/instance-scheduler), [aws/finops-cost-report](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/finops-cost-report)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/instance-scheduler | Ambientes de dev e homologação ligados à noite e no fim de semana. | Desligar por tag com agenda de horário comercial. |
| aws/tag-compliance | Custo sem dono, que ninguém consegue cortar. | Tags obrigatórias aplicadas na criação, não na revisão do mês. |

Os valores variam com região e volume; a tabela mostra onde olhar primeiro.

## Veja também

- [Módulo principal no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/tag-compliance/README.md)
- [Mapa de experiência AWS no monorepo](https://github.com/Raphaelfcs/automacao_terraform#experi%C3%AAncia-pr%C3%A1tica-na-aws-onde-est%C3%A1-no-c%C3%B3digo)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
