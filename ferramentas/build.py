"""Monta o jogo: castelos.py -> src/castelos.js -> template -> index.html (com a folha de sprites embutida).
Uso (na raiz do repositório):
    python3 ferramentas/gerar_brasa.py   # só se mudar os sprites
    python3 ferramentas/build.py
"""
import json, base64, re, os, shutil, subprocess, sys
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = lambda *a: os.path.join(RAIZ, *a)
subprocess.run([sys.executable, P('ferramentas', 'castelos.py')], check=True)
tpl = open(P('src', 'lenda-da-brasa.template.html'), encoding='utf-8').read()
gen = open(P('src', 'castelos.js'), encoding='utf-8').read()
ini = tpl.index('// ==== CASTELOS (gerado por castelos.py) ====')
fim = tpl.index('const MAPS={', ini)
tpl = tpl[:ini] + gen + tpl[fim:]
open(P('src', 'lenda-da-brasa.template.html'), 'w', encoding='utf-8').write(tpl)
a = json.load(open(P('sprites', 'lenda-da-brasa-atlas.json'), encoding='utf-8'))['sprites']
atlas = {k: [v['x'], v['y'], v['w'], v['h']] for k, v in a.items()}
b64 = base64.b64encode(open(P('sprites', 'lenda-da-brasa-sprites.png'), 'rb').read()).decode()
out = tpl.replace('__SHEET_B64__', b64).replace('__ATLAS__', json.dumps(atlas, separators=(',', ':')))
head = '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
open(P('index.html'), 'w', encoding='utf-8').write(head + out + '\n</html>\n')
shutil.copy(P('sprites', 'lenda-da-brasa-sprites.png'), P('lenda-da-brasa-sprites.png'))
print('index.html gerado')
