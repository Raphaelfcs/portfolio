# Rede AWS hub-and-spoke: VPC, Transit Gateway, VPN e Direct Connect

*Uma conta Network, rotas segmentadas por ambiente e conectividade híbrida com contingência, tudo como código.*

Raphael Santos · 4 min de leitura · AWS na prática

![aws/network-hub: Conta Network hub-and-spoke](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-pt-1.webp)

> **Em resumo:** Peering entre VPCs funciona até a décima conta. Depois disso, a rede precisa de um hub, de rotas segmentadas e de alguém dono do plano de endereçamento.

## O problema

Com muitas contas, peering vira uma malha impossível de auditar, CIDRs se sobrepõem e o tráfego de produção passa a enxergar o de desenvolvimento. A conexão com o datacenter ou com parceiros fica em cada VPC, cada uma com sua VPN.

## A solução

Uma conta Network concentra o Transit Gateway, compartilhado por RAM com a organização. As tabelas de rota separam prod, nonprod e shared: cada VPC spoke se associa ao seu domínio e só propaga para onde pode. A conectividade híbrida entra pelo hub, com Direct Connect por transit VIF e VPN Site-to-Site com BGP como contingência. Nas VPCs, três camadas por AZ, a de dados sem rota para a internet, e VPC endpoints para falar com serviços AWS sem passar por NAT.

### Como montar

1. Planeje o endereçamento (IPAM) antes do primeiro attachment: CIDR duplicado no mesmo TGW deixa o destino imprevisível.
2. Crie a conta Network e compartilhe o Transit Gateway por RAM com a organização.
3. Separe as tabelas de rota por domínio: prod, nonprod e shared, com associação e propagação explícitas.
4. Anexe cada VPC spoke e crie, nas tabelas privadas, as rotas para os CIDRs remotos via TGW.
5. Ligue o Direct Connect por transit VIF e a VPN com BGP como caminho de contingência.
6. Use VPC endpoints para ECR, STS, logs e SSM, e endpoint gateway para S3, reduzindo o tráfego por NAT.

> **Nota:** Integrei a rede de um parceiro pelo mesmo modelo: um attachment dedicado, numa tabela de rota própria, sem enxergar as demais VPCs.

![Figura 2: aws/vpc: VPC em três camadas](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-pt-2.webp)
*Figura 2: aws/vpc: VPC em três camadas*

![Figura 3: aws/vpn-site-to-site: VPN Site-to-Site (TGW/VGW) declarativa](https://raphaelfcs.github.io/portfolio/artigos/img/aws-rede-hub-and-spoke-pt-3.webp)
*Figura 3: aws/vpn-site-to-site: VPN Site-to-Site (TGW/VGW) declarativa*

## O código

```hcl
module "vpn_site_to_site" {
  source = "git::https://github.com/Raphaelfcs/automacao_terraform.git//aws/vpn-site-to-site?ref=main"

  transit_gateway_route_table_id = "tgw-rtb-0123456789abcdef0"
  vpn_connections = {
    matriz = {
      target_gateway_type = "transit_gateway"
      transit_gateway_id  = "tgw-0123456789abcdef0"
      routing_option      = "dynamic"
      customer_gateway    = { mode = "new", bgp_asn = 65010, ip_address = "203.0.113.10" }
    }
  }
  tags = local.tags
}
```

## Discussão

**Módulos Terraform usados:** [aws/network-hub](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/network-hub), [aws/vpc](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc), [aws/transit-gateway-attachment](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/transit-gateway-attachment), [aws/vpn-site-to-site](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpn-site-to-site), [aws/vpc-endpoints](https://github.com/Raphaelfcs/automacao_terraform/tree/main/aws/vpc-endpoints)

### FinOps: onde está o custo

| Componente | O que pesa | Alavanca |
|---|---|---|
| aws/network-hub | Hora por attachment do TGW e GB processado. | Consolidar VPCs pequenas e evitar tráfego entre ambientes que não precisa existir. |
| aws/vpc-endpoints | NAT Gateway cobrando por GB para falar com serviços AWS. | Endpoint gateway de S3 (gratuito) e interface só para os serviços de alto volume. |
| aws/vpn-site-to-site | Hora por conexão VPN. | VPN como contingência do Direct Connect, não como caminho principal. |

Os valores variam com região e volume; a tabela mostra onde olhar primeiro.

## Veja também

- [Módulo principal no GitHub](https://github.com/Raphaelfcs/automacao_terraform/blob/main/aws/network-hub/README.md)
- [Mapa de experiência AWS no monorepo](https://github.com/Raphaelfcs/automacao_terraform#experi%C3%AAncia-pr%C3%A1tica-na-aws-onde-est%C3%A1-no-c%C3%B3digo)
- [Todos os artigos](https://raphaelfcs.github.io/portfolio/artigos/)

---

*Raphael Santos é Lead Cloud Architect, com mais de 9 anos em DevOps e arquitetura de nuvem em AWS, Google Cloud e Azure. Todo o código deste artigo está no GitHub.*

*Nomes de empresas, contas e IDs foram removidos; os valores do código são fictícios.*
