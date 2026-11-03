# Integração de rede com parceiro

*Peering de Transit Gateways para sinalização Diameter e dados em sub-redes privadas.*

Raphael Santos · 3 min de leitura · CCoE, landing zone e plataforma de uma operadora de telecom (2025-2026)

![Integração de rede com parceiro via Transit Gateway](https://raphaelfcs.github.io/portfolio/artigos/img/integracao-rede-parceiro-pt-1.webp)

> **Em resumo:** Integrar a rede de um parceiro sem misturar responsabilidades.

## O problema

Plataforma precisando consumir e expor serviços para a rede de um parceiro.

## A solução

Transit Gateway como ponto único, DNS privado entre os lados e serviços de dados (Kafka, Redis, banco) só em subnets privadas.

### Integração de rede com parceiro via Transit Gateway

1. Peers de sinalização entram pela rede do parceiro.
2. Peering entre Transit Gateways.
3. Tráfego SCTP chega ao gateway no EKS.
4. Dados só em sub-redes privadas.

> **Nota:** Medido na conta (varredura read-only), não inferido do código.

## O código

```hcl
module "kms_key" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/kms-key"

  name_prefix             = local.name_prefix
  deletion_window_in_days = 7
  tags                    = local.tags
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

## Discussão

**Módulos Terraform usados:** [aws/kms-key](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/kms-key), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/route53-private-zone](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/route53-private-zone), [aws/msk-kafka](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/msk-kafka), [aws/elasticache-redis](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/elasticache-redis), [aws/rds-instance](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/rds-instance)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/rds-instance | classe da instância e Multi-AZ do RDS | dimensionar pela métrica real, reserva para PRD e parar HML/DEV fora do horário |
| aws/msk-kafka | brokers e armazenamento do MSK | retenção por tópico, tiered storage e brokers Graviton |
| aws/vpc | NAT Gateway por AZ e tráfego que passa por ele | um NAT só em DEV e VPC endpoints para S3/ECR tirarem tráfego do NAT |
| aws/transit-gateway-attachment | attachments e GB processados no Transit Gateway | consolidar attachments e manter tráfego de alto volume fora do TGW |

No repositório, aws/tag-compliance, aws/finops-cost-report, aws/cur-focus-export e aws/instance-scheduler fecham o ciclo: tags obrigatórias, relatório de custo, export CUR/FOCUS e agenda de desligamento.

## Veja também

- [Lab completo no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/integracao-rede-parceiro/README.md)
- [Processo de FinOps](https://github.com/Raphaelfcs/automacao_terraform/blob/main/labs/arquiteturas/telecom/processo-finops/README.md)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
