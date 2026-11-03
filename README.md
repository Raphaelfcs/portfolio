# Raphael Santos · Portfólio / Portfolio

🇧🇷 Portfólio de **Raphael Santos**, Lead Cloud Architect (DevOps · FinOps · AWS · Google Cloud · Azure).
🇺🇸 Portfolio of **Raphael Santos**, Lead Cloud Architect (DevOps · FinOps · AWS · Google Cloud · Azure).

O site é uma página estática bilíngue (PT/EN) com trajetória, linha do tempo dos projetos, arquiteturas em destaque e certificações verificáveis.
The site is a static bilingual page (PT/EN) with career history, project timeline, featured architectures and verifiable certifications.

| | |
|---|---|
| Código das arquiteturas / Architecture code | [Raphaelfcs/automacao_terraform](https://github.com/Raphaelfcs/automacao_terraform) |
| LinkedIn | [raphael-ferreira-coelho-santos](https://www.linkedin.com/in/raphael-ferreira-coelho-santos/) |

## Estrutura / Structure

```
index.html          página gerada / generated page (abra no navegador / open in the browser)
assets/             foto e desenhos das arquiteturas em WebP / photo and architecture diagrams (WebP)
src/page.html       conteúdo, estilos e scripts / content, styles and scripts
src/head.html       cabeçalho HTML / HTML head
src/data.json       labs do monorepo (títulos, descrições, nuvem, módulos) / monorepo labs data
tools/build.py      monta o index.html / builds index.html
```

```bash
python3 tools/build.py   # regenera / regenerates index.html
```

Sem dependências: só HTML, CSS e JavaScript, com fontes do Google Fonts. Pronto para GitHub Pages, Cloudflare Pages ou S3 + CloudFront.
No dependencies: plain HTML, CSS and JavaScript, with Google Fonts. Ready for GitHub Pages, Cloudflare Pages or S3 + CloudFront.
