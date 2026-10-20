# Fuente del Plan Completo (almuerzos y cenas para congelar) y de las recetas de
# los bonos (loncheras, batidos y meriendas). Genera extras.js para la app.
# Las recetas están en extras/*.py; cada archivo define LISTA y PLURALES.
# ⚠ Pendiente: revisión de la nutricionista antes del lanzamiento.
import json, os, re, glob

COMIDAS = ['pollo', 'res', 'cerdo', 'pescado', 'legumbres', 'sopas', 'pastas']
ESPERADO = {'comida': 150, 'lonchera': 20, 'batido': 15, 'merienda': 20}
PAN = re.compile(r'\bpan\b|\bpanes\b|pan rallado|pan molido|tostada|tortilla(s)? de (harina|maíz)|\barepa|empanada|hojaldre|\bwrap|\bbollo', re.I)

def R(id, nombre, cat, minutos, porciones, ingredientes, pasos, congela=None, noche=None):
    r = dict(id=id, nombre=nombre, col='comida' if cat in COMIDAS else cat, tipo=cat, min=minutos, porciones=porciones,
             ing=[list(i) for i in ingredientes], pasos=[list(p) for p in pasos])
    if congela: r['congela'] = list(congela)
    if noche: r['noche'] = noche
    return r

AQUI = os.path.dirname(os.path.abspath(__file__))
EXTRAS, PLURALES = [], {}
for ruta in sorted(glob.glob(f'{AQUI}/extras/*.py')):
    g = {'R': R}; exec(open(ruta, encoding='utf-8').read(), g)
    EXTRAS += g['LISTA']; PLURALES.update({k: list(v) for k, v in g.get('PLURALES', {}).items()})

desayunos = open(f'{AQUI}/recetas.js', encoding='utf-8').read()
ids_desayunos = set(r['id'] for r in json.loads(desayunos[desayunos.index('['):desayunos.rindex(']') + 1]))
# Comidas en el orden de sus categorías; los bonos al final.
ORDEN = COMIDAS + ['lonchera', 'batido', 'merienda']
EXTRAS.sort(key=lambda r: ORDEN.index(r['tipo']))
ids = [r['id'] for r in EXTRAS]
assert len(ids) == len(set(ids)), 'ids repetidos: ' + str({i for i in ids if ids.count(i) > 1})
assert not ids_desayunos & set(ids), 'choca con un desayuno: ' + str(ids_desayunos & set(ids))
assert not [r['id'] for r in EXTRAS if PAN.search(r['nombre'] + ' ' + ' '.join(i[2] for i in r['ing']))], 'hay pan'
cuenta = {}
for r in EXTRAS: cuenta[r['col']] = cuenta.get(r['col'], 0) + 1
assert cuenta == ESPERADO, cuenta

open(f'{AQUI}/extras.js', 'w', encoding='utf-8').write(
    '// Generado desde extras.py — no editar a mano.\nwindow.EXTRAS = ' + json.dumps(EXTRAS, ensure_ascii=False) +
    ';\nwindow.PLURALES_EXTRA = ' + json.dumps(PLURALES, ensure_ascii=False) + ';\n')
print(len(EXTRAS), 'recetas', cuenta, {c: sum(r['tipo'] == c for r in EXTRAS) for c in COMIDAS})
