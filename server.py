"""Lokalny dev server dla AI Research Playground.

Zastępuje 'python3 -m http.server 8080'.
Serwuje pliki statyczne + endpointy API do zarządzania platformami.

Uruchomienie:
    python3 server.py
"""
import json, os, re, textwrap
import pathlib
from flask import Flask, request, jsonify, send_from_directory

ROOT = pathlib.Path(__file__).parent
app  = Flask(__name__, static_folder=str(ROOT), static_url_path='')

# ── STATIC ────────────────────────────────────────────────────────────────────
@app.route('/')
def index(): return send_from_directory(ROOT, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    try: return send_from_directory(ROOT, path)
    except Exception: return '', 404

# ── TEMPLATES ─────────────────────────────────────────────────────────────────
def tpl_readme(name, url, key_var, types_str):
    return textwrap.dedent(f"""\
        # {name}

        ## Dane platformy
        | | Wartość |
        |---|---|
        | **API base** | `{url}` |
        | **Auth** | `Authorization: Bearer <{key_var}>` |
        | **Typy** | {types_str} |

        ## Szybki start
        ```bash
        cp .env.example .env   # uzupełnij {key_var}
        pip install requests python-dotenv
        python scripts/list_models.py
        python text/chat.py "Twoje pytanie"
        ```

        ## Status
        - [ ] Klucz API skonfigurowany ({key_var} w .env)
        - [ ] Połączenie zweryfikowane
    """)

def tpl_env_example(name, url, key_var):
    return f"# {name}\n{key_var}=\n{name.upper()}_BASE_URL={url}\n"

def tpl_gitignore():
    return ".env\noutput/*\n!output/.gitkeep\n__pycache__/\n*.pyc\n"

def tpl_list_models(name, url, key_var):
    return textwrap.dedent(f"""\
        \"\"\"Listowanie modeli {name} — sanity-check połączenia.\"\"\"
        import os, sys
        import requests
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
        api_key  = os.getenv("{key_var}")
        base_url = os.getenv("{name.upper()}_BASE_URL", "{url}")

        if not api_key:
            sys.exit("❌ Brak {key_var} w .env (skopiuj .env.example → .env).")

        headers = {{"Authorization": f"Bearer {{api_key}}"}}

        try:
            r = requests.get(f"{{base_url}}/models", headers=headers, timeout=30)
            print(f"Status: {{r.status_code}}")
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            sys.exit(f"❌ Błąd: {{e}}\\n{{getattr(e.response,'text','')[:200]}}")

        data = r.json()
        models = data if isinstance(data, list) else data.get("data", [])
        print(f"✅ Modeli: {{len(models)}}\\n")
        for m in sorted(models, key=lambda x: x.get("id", x.get("name", ""))):
            print(f"  {{m.get('id', m.get('name', m))}}")
    """)

def tpl_chat(name, url, key_var):
    return textwrap.dedent(f"""\
        \"\"\"Czat z {name} (OpenAI-compatible).

        Użycie:
            python text/chat.py "Twoje pytanie"
        \"\"\"
        import os, sys
        import requests
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
        API_KEY  = os.getenv("{key_var}")
        BASE_URL = os.getenv("{name.upper()}_BASE_URL", "{url}")
        MODEL    = os.getenv("{name.upper()}_MODEL", "")

        if not API_KEY:
            sys.exit("❌ Brak {key_var} w .env")

        prompt = sys.argv[1] if len(sys.argv) > 1 else "Czesc, kim jestes? Odpowiedz krotko."
        if not MODEL:
            print("⚠️  Brak {name.upper()}_MODEL w .env — wpisz model jako drugi argument lub uzupełnij .env")
            MODEL = sys.argv[2] if len(sys.argv) > 2 else ""
            if not MODEL:
                sys.exit("❌ Podaj nazwę modelu jako sys.argv[2] lub ustaw {name.upper()}_MODEL w .env")

        headers = {{"Authorization": f"Bearer {{API_KEY}}", "Content-Type": "application/json"}}
        r = requests.post(f"{{BASE_URL}}/chat/completions", headers=headers,
            json={{"model": MODEL, "messages": [{{"role": "user", "content": prompt}}]}},
            timeout=120)
        print(f"Status: {{r.status_code}}")
        if r.status_code == 200:
            d = r.json()
            print(f"✅ Model: {{d.get('model')}}")
            print(d["choices"][0]["message"]["content"])
            print("Tokeny:", d.get("usage"))
        else:
            print("Treść:", r.text[:400])
    """)

# ── API: ADD PROVIDER ──────────────────────────────────────────────────────────
@app.post('/api/add-provider')
def add_provider():
    data    = request.json or {}
    name    = data.get('name', '').strip()
    url     = data.get('url', '').strip()
    key_val = data.get('key', '').strip()
    compat  = data.get('compat', 'openai')
    types   = data.get('types', ['text'])

    if not name or not re.match(r'^[A-Za-z][A-Za-z0-9_\-]*$', name):
        return jsonify({'ok': False, 'error': 'Nieprawidłowa nazwa (zacznij od litery, tylko [A-Za-z0-9_-])'}), 400
    if not url:
        return jsonify({'ok': False, 'error': 'Brak URL'}), 400

    base    = ROOT / name
    key_var = f"{name.upper().replace('-','_')}_API_KEY"
    types_str = ' · '.join(t.capitalize() for t in types)

    # Dirs
    (base / 'scripts').mkdir(parents=True, exist_ok=True)
    if 'text'  in types: (base / 'text').mkdir(exist_ok=True)
    if 'image' in types: (base / 'image').mkdir(exist_ok=True)
    if 'video' in types: (base / 'video').mkdir(exist_ok=True)
    if 'audio' in types: (base / 'audio').mkdir(exist_ok=True)
    (base / 'output').mkdir(exist_ok=True)
    (base / 'output' / '.gitkeep').touch()

    # Core files
    (base / 'README.md').write_text(tpl_readme(name, url, key_var, types_str))
    (base / '.env.example').write_text(tpl_env_example(name, url, key_var))
    (base / '.gitignore').write_text(tpl_gitignore())

    if key_val:
        (base / '.env').write_text(f"{key_var}={key_val}\n{name.upper()}_BASE_URL={url}\n")

    # Scripts
    if compat == 'openai':
        (base / 'scripts' / 'list_models.py').write_text(tpl_list_models(name, url, key_var))
        if 'text' in types:
            (base / 'text' / 'chat.py').write_text(tpl_chat(name, url, key_var))

    # Update keys.json
    kp = ROOT / 'keys.json'
    k  = json.loads(kp.read_text()) if kp.exists() else {}
    k[name.lower()] = key_val
    kp.write_text(json.dumps(k, indent=2))

    # Update make_config.py — append new provider
    _append_to_make_config(name, key_var)

    return jsonify({
        'ok': True,
        'path': str(base),
        'key_var': key_var,
        'files': [str(f.relative_to(ROOT)) for f in base.rglob('*') if f.is_file()]
    })

def _append_to_make_config(name, key_var):
    """Dodaje nową platformę do make_config.py jeśli jeszcze jej nie ma."""
    mc = ROOT / 'make_config.py'
    if not mc.exists(): return
    src = mc.read_text()
    entry = f'    "{name.lower()}":  env("{name}/.env", "{key_var}"),'
    if key_var in src: return
    marker = '}\n\nout ='
    src = src.replace(marker, f'    {entry}\n{marker}')
    mc.write_text(src)

# ── API: PROVIDER INFO ────────────────────────────────────────────────────────
@app.get('/api/provider/<name>')
def get_provider_info(name):
    from dotenv import dotenv_values
    base = ROOT / name
    if not base.exists() or not (base / 'README.md').exists():
        return jsonify({'ok': False, 'error': f'Provider {name} not found'}), 404

    env_path = base / '.env'
    ev = dict(dotenv_values(env_path)) if env_path.exists() else {}
    slug = name.upper().replace('-', '_')

    key_var  = f"{slug}_API_KEY"
    key_val  = ev.get(key_var) or next((ev[k] for k in ev if k.endswith('_API_KEY')), '')
    base_url = ev.get(f"{slug}_BASE_URL") or next((ev[k] for k in ev if 'BASE_URL' in k), '')

    return jsonify({
        'ok': True,
        'name': name,
        'key_var': key_var,
        'key': key_val or '',
        'base_url': base_url or '',
        'has_chat': (base / 'text' / 'chat.py').exists(),
        'has_list_models': (base / 'scripts' / 'list_models.py').exists(),
    })

# ── API: LIST PROVIDERS ────────────────────────────────────────────────────────
@app.get('/api/providers')
def list_providers():
    kp = ROOT / 'keys.json'
    keys = json.loads(kp.read_text()) if kp.exists() else {}
    providers = []
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and not d.name.startswith('.') and (d / 'README.md').exists():
            providers.append({
                'name': d.name,
                'has_key': bool(keys.get(d.name.lower())),
                'has_env': (d / '.env').exists(),
            })
    return jsonify(providers)

if __name__ == '__main__':
    print("🚀 AI Research Playground — http://localhost:8080")
    print("   API: POST /api/add-provider | GET /api/providers | GET /api/provider/<name>")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
