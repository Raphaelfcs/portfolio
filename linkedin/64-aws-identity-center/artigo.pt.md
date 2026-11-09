# IAM Identity Center como código: acesso sem usuário IAM

*Grupos, permission sets e atribuições versionados em Terraform, com break-glass separado e pipelines por OIDC.*

Raphael Santos · 3 min de leitura · AWS na prática

![aws/identity-center-permission-set: IAM Identity Center: permission sets e atribuições](https://raphaelfcs.github.io/portfolio/artigos/img/aws-identity-center-pt-1.webp)

> **Em resumo:** Em ambiente multi-conta, cada usuário IAM é uma chave de longa duração esperando vazar. O acesso humano fica no IAM Identity Center, e o acesso de pipeline, em OIDC.

## O problema

O cenário típico: dezenas de contas, usuários IAM criados conta a conta, chaves de acesso antigas e ninguém sabendo quem acessa o quê. Auditoria vira planilha, e desligar alguém leva dias.

## A solução

Grupos no diretório do Identity Center (ou sincronizados do IdP corporativo), permission sets com políticas gerenciadas, inline, customer managed e permissions boundary, e atribuições grupo para conta, tudo em Terraform. Revisar acesso passa a ser revisar um pull request. Usuário IAM sobra só para break-glass e integrações legadas, e as pipelines assumem roles por OIDC, sem chave fixa.

### Como montar

1. Defina os grupos por função, não por pessoa: admins da plataforma, devs, somente leitura, FinOps.
2. Crie os permission sets com o menor privilégio e duração de sessão curta para os de escrita.
3. Atribua grupo para conta com base em OU e ambiente: escrita em dev, leitura em prd.
4. Use delegated administrator para não operar o Identity Center a partir da conta de gerenciamento.
5. Mantenha um grupo IAM de break-glass com MFA e alerta de uso, fora do Identity Center.
6. Troque as chaves das pipelines por roles assumidas via OIDC, uma de plan e outra de deploy com aprovação.

> **Nota:** Mudança em permission set é reprovisionada em todas as contas atribuídas. Teste em uma conta de sandbox antes.

![Figura 2: aws/identity-center-groups: IAM Identity Center: grupos e usuários](https://raphaelfcs.github.io/portfolio/artigos/img/aws-identity-center-pt-2.webp)
*Figura 2: aws/identity-center-groups: IAM Identity Center: grupos e usuários*

## O código

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

## Discussão

**Módulos Terraform usados:** [aws/identity-center-groups](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/identity-center-groups), [aws/identity-center-permission-set](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/identity-center-permission-set), [aws/iam-group](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-group), [aws/iam-github-oidc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/iam-github-oidc)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/identity-center-permission-set | Nada: o Identity Center não cobra por usuário. | Menos tempo de operação com acessos e auditorias. |
| aws/iam-github-oidc | Nada: OIDC não tem custo. | Elimina rotação de chaves e o risco de vazamento. |

Os valores variam com região e volume; a tabela mostra onde olhar primeiro.

## Veja também

- [Módulo principal no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/identity-center-groups/README.md)
- [Mapa de experiência AWS no monorepo](https://github.com/Raphaelfcs/automacao_terraform#experi%C3%AAncia-pr%C3%A1tica-na-aws-onde-est%C3%A1-no-c%C3%B3digo)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
