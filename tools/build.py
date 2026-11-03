"""Monta index.html a partir de src/page.html + src/data.json (dados dos labs do monorepo automacao_terraform)."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
body = (root / 'src/page.html').read_text().replace('/*DATA*/null', json.dumps(json.loads((root / 'src/data.json').read_text()), ensure_ascii=False))
head = (root / 'src/head.html').read_text()
i = body.index('<nav')
(root / 'index.html').write_text(head + body[:i] + '</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n')
print('index.html gerado')
