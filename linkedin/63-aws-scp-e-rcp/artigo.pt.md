# SCP e RCP: o perímetro de dados da organização AWS

*Uma limita o que as suas identidades fazem; a outra, quem chega aos seus recursos. Como uso as duas em landing zones multi-conta.*

Raphael Santos · 4 min de leitura · AWS na prática

![aws/organizations-scp: Organizations: OUs, SCPs, RCPs e Tag Policy](https://raphaelfcs.github.io/portfolio/artigos/img/aws-scp-e-rcp-pt-1.webp)

> **Em resumo:** SCP sozinha não impede que uma conta de fora leia o seu bucket. RCP sozinha não impede que alguém de dentro desligue o CloudTrail. O perímetro de dados precisa das duas.

## O problema

Em landing zones multi-conta, o risco mais comum não é o ataque sofisticado: é a bucket policy aberta por engano, a role confiando numa conta de fornecedor esquecida, o time que cria recurso em região não permitida. SCP resolve o lado das identidades da organização, mas não alcança quem está fora dela.

## A solução

As SCPs ficam nas OUs: região permitida, proteção de CloudTrail, GuardDuty, Config e Security Hub, root negado, criptografia obrigatória e tags na criação. As RCPs, lançadas pela AWS no fim de 2024, fecham o outro lado: S3, STS, KMS, SQS e Secrets Manager só aceitam identidades da própria organização, serviços AWS e contas confiáveis declaradas, sempre com TLS. Um budget estourado aplica uma SCP de congelamento. Tudo em Terraform, com testes que validam o conteúdo das políticas.

### Como montar

1. Desenhe as OUs antes das políticas: Security, Infrastructure, Workloads (Prod e NonProd), Sandbox e Suspended.
2. Anexe as SCPs de proteção às OUs e isente só as roles do Control Tower, do AFT e do break-glass.
3. Habilite o tipo RESOURCE_CONTROL_POLICY na raiz e anexe as RCPs primeiro numa OU de sandbox.
4. Declare as contas de fora que realmente precisam de acesso (parceiro, backup) em rcp_trusted_accounts; o resto é negado.
5. Ligue o budget-guardrail: ao atingir o teto, uma SCP nega criar ou ligar recursos caros até alguém revisar.

> **Nota:** SCP e RCP não se aplicam à conta de gerenciamento. Por isso ela não roda carga de trabalho.

![Figura 2: aws/budget-guardrail: FinOps: teto de custo com congelamento por SCP](https://raphaelfcs.github.io/portfolio/artigos/img/aws-scp-e-rcp-pt-2.webp)
*Figura 2: aws/budget-guardrail: FinOps: teto de custo com congelamento por SCP*

## O código

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

## Discussão

**Módulos Terraform usados:** [aws/organizations-scp](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/organizations-scp), [aws/budget-guardrail](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/budget-guardrail), [aws/control-tower-ou-registration](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/control-tower-ou-registration)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/organizations-scp | Nada: SCP, RCP e Tag Policy não têm custo. | A Tag Policy padroniza CentroCusto e Dono, base do custo por time. |
| aws/budget-guardrail | Gasto que só é visto na fatura do mês seguinte. | Alerta pela previsão e congelamento automático pela SCP. |

Os valores variam com região e volume; a tabela mostra onde olhar primeiro.

## Veja também

- [Módulo principal no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/organizations-scp/README.md)
- [Mapa de experiência AWS no monorepo](https://github.com/Raphaelfcs/automacao_terraform#experi%C3%AAncia-pr%C3%A1tica-na-aws-onde-est%C3%A1-no-c%C3%B3digo)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
