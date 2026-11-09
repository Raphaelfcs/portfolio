# EventBridge e Lambda: integração entre contas que aguenta falha

*Barramento dedicado, fila com DLQ, archive para replay e alarmes que avisam antes do cliente.*

Raphael Santos · 4 min de leitura · AWS na prática

![aws/eventbridge-bus-sqs: Barramento de eventos entre contas -> SQS](https://raphaelfcs.github.io/portfolio/artigos/img/aws-eventbridge-lambda-pt-1.webp)

> **Em resumo:** Integração por evento só é confiável quando você sabe o que acontece com a mensagem que falhou. Sem DLQ, archive e alarme, o evento simplesmente some.

## O problema

Um produtor em outra conta (um parceiro, outro time) precisa avisar o seu sistema de que algo aconteceu. A primeira versão costuma ser uma chamada HTTP direta: quando o consumidor cai, o evento se perde e ninguém percebe até o cliente reclamar.

## A solução

O produtor publica num barramento EventBridge dedicado, liberado por resource policy só para as roles dele. Uma regra filtra por source e detail-type e entrega numa fila SQS cifrada com KMS, com DLQ para a regra e para a fila. O archive guarda os eventos e permite replay sem depender do produtor. Lambdas consomem a fila com menor privilégio, DLQ e X-Ray, e os alarmes cobrem consumidor parado, mensagem antiga, DLQ com itens e falha de entrega da regra.

### Como montar

1. Crie um barramento por domínio de integração e libere PutEvents só para as roles do produtor.
2. Filtre na regra por source e detail-type; não deixe o consumidor descobrir o que ignorar.
3. Entregue em SQS cifrada, com DLQ na regra (falha de entrega) e na fila (falha de processamento).
4. Ligue o archive com retenção definida para poder reprocessar depois de um bug.
5. Consuma com Lambda de menor privilégio, batch size ajustado e relatório de falhas parciais.
6. Alarme em idade da mensagem mais antiga, profundidade da DLQ e FailedInvocations da regra.

> **Nota:** Para tarefas agendadas uso o EventBridge Scheduler, que aceita fuso horário: 7h em São Paulo continua 7h no horário de verão de outro país.

![Figura 2: aws/lambda-function: Função Lambda empacotada](https://raphaelfcs.github.io/portfolio/artigos/img/aws-eventbridge-lambda-pt-2.webp)
*Figura 2: aws/lambda-function: Função Lambda empacotada*

## O código

```hcl
module "eventbridge_bus_sqs" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/eventbridge-bus-sqs?ref=main"

  name_prefix             = local.name_prefix
  queue_name              = "pedidos"
  event_sources           = ["parceiro.pedidos"]
  detail_types            = ["PedidoConcluido"]
  producer_principal_arns = ["arn:aws:iam::210987654321:role/parceiro-eventbridge"]
  kms_key_arn             = "arn:aws:kms:sa-east-1:123456789012:key/11111111-2222-3333-4444-555555555555"
  consumer_role_name      = "demo-dev-consumidor"
  alarm_actions           = ["arn:aws:sns:sa-east-1:123456789012:demo-dev-alertas"]
  tags                    = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/eventbridge-bus-sqs](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/eventbridge-bus-sqs), [aws/lambda-function](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/lambda-function), [aws/sqs-queue](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sqs-queue), [aws/sns-topic](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/sns-topic)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/eventbridge-bus-sqs | Eventos publicados em barramento customizado e GB arquivado. | Filtrar na origem e definir a retenção do archive. |
| aws/lambda-function | GB-segundo de execução e logs sem retenção. | Memória ajustada por medição e log group com retenção e KMS. |

Os valores variam com região e volume; a tabela mostra onde olhar primeiro.

## Veja também

- [Módulo principal no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/eventbridge-bus-sqs/README.md)
- [Mapa de experiência AWS no monorepo](https://github.com/Raphaelfcs/automacao_terraform#experi%C3%AAncia-pr%C3%A1tica-na-aws-onde-est%C3%A1-no-c%C3%B3digo)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
