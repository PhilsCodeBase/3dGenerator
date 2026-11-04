import base64, json, os, shutil, sys
A='/home/claude/app'; SRC='/home/claude/src'
models = {'blazeface.json':f'{SRC}/human/models/blazeface.json','blazeface.bin':f'{SRC}/human/models/blazeface.bin',
 'facemesh.json':f'{SRC}/human/models/facemesh.json','facemesh.bin':f'{SRC}/human/models/facemesh.bin',
 'rvm.json':f'{SRC}/human-models/models/rvm.json','rvm.bin':f'{SRC}/human-models/models/rvm.bin'}
libs = {'THREE':f'{SRC}/three/build/three.min.js','ORBIT':f'{SRC}/three/examples/js/controls/OrbitControls.js','HUMAN':f'{SRC}/human/dist/human.js'}
html = open(f'{A}/app.html').read()
for k,p in libs.items():
    js = open(p).read()
    assert '</script' not in js.lower(), k
    html = html.replace(f'/*@@{k}@@*/', js)
art = html.replace('/*@@MODELS@@*/','window.__MODEL_BIN_SUFFIX=".wasm";')
os.makedirs(f'{A}/dist/artifact/models', exist_ok=True)
open(f'{A}/dist/artifact/index.html','w').write(art)
shutil.rmtree(f'{A}/dist/artifact/models'); os.makedirs(f'{A}/dist/artifact/models')
for n,p in models.items(): shutil.copy(p, f'{A}/dist/artifact/models/{n}' + ('.wasm' if n.endswith('.bin') else ''))
emb = {n: base64.b64encode(open(p,'rb').read()).decode() for n,p in models.items()}
std = html.replace('/*@@MODELS@@*/', 'window.__EMBED_MODELS=' + json.dumps(emb) + ';')
std = '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style></head><body>' + std + '</body></html>'
open(f'{A}/dist/Bildhauer-3D.html','w').write(std)
print(len(art)//1024, 'KB artifact page;', len(std)//1024, 'KB standalone')
