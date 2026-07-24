# ---
# operator: artificer
# agent: alchemist.Haldir
# session: 92d0faba-45d4-473e-93a4-e05ae658cd4b
# created: 2026-07-20
# origin: BUILD unDolphin -- the real local image-gen app. Backend engine: a thin Flask server that
#         serves the UI and routes generation to a real provider. Provider = Runware task-array API
#         (vault key). Provider swap-in later: local ComfyUI on the OCI GPU. The UI never changes
#         when the backend provider changes. 0.2.0 adds seed/reference images (upload -> UUID ->
#         seedImage on the inference task), per the App2 design mockup.
# location: _DECK 8\LAB 70 - unDolphin\CODE\app.py
# release_status: draft
# version: 0.2.0
# ---

import base64
import glob
import io
import json
import os
import re
import time
import uuid

import requests
from flask import Flask, request, jsonify, send_from_directory, send_file

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "static")
STATE = os.path.join(HERE, "state")


def _output_dir():
    # outputs live in the unDolphin STORE, not in CODE. Resolve by the beacon marker, never a
    # frozen path -- find !UNDOLPHIN_ROOT.md, its parent = the store, join OUTPUT.
    hits = glob.glob(r"C:\_INFRA\_STORES\**\!UNDOLPHIN_ROOT.md", recursive=True)
    if hits:
        return os.path.join(os.path.dirname(hits[0]), "OUTPUT")
    return os.path.join(HERE, "gallery")  # fallback if the store is unreachable


def _slugify(text, maxlen=48):
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:maxlen].rstrip("-")


GALLERY = _output_dir()
for d in (GALLERY, STATE):
    os.makedirs(d, exist_ok=True)

app = Flask(__name__, static_folder=None)

# ---- credentials: pull the Runware key once, from the vault ----
_KEY = {"runware": None}


def runware_key():
    if _KEY["runware"] is None:
        r = requests.post(os.environ["VAULT_URL"] + "/credential",
                          json={"name": "runware_api_key"},
                          headers={"X-Vault-Key": os.environ["VAULT_KEY"]}, timeout=10)
        r.raise_for_status()
        _KEY["runware"] = r.json()["value"]
    return _KEY["runware"]


def load_models():
    with open(os.path.join(HERE, "models.json"), encoding="utf-8") as f:
        return json.load(f)


MODELS = load_models()
MODEL_BY_ID = {m["id"]: m for m in MODELS}

RUNWARE_URL = "https://api.runware.ai/v1"


# ---- generation: Runware task-array API (Flux / SDXL / Kling / Grok, per-image) ----
def _runware_call(task):
    try:
        r = requests.post(RUNWARE_URL, headers={"Authorization": "Bearer " + runware_key()},
                          json=[task], timeout=120)
        body = r.json()
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, str(e)[:200])
    if r.status_code == 200 and "data" in body and body["data"]:
        return body["data"][0], None
    return None, str(body.get("errors") or body)[:300]


def runware_generate(air, prompt, negative, width, height, steps, seed, ref=None):
    task = {
        "taskType": "imageInference", "taskUUID": str(uuid.uuid4()),
        "positivePrompt": prompt, "model": air,
        "width": int(width), "height": int(height),
        "numberResults": 1, "outputType": "URL",
    }
    if ref:
        task["seedImage"] = ref
    if steps:
        task["steps"] = int(steps)
    if negative:
        task["negativePrompt"] = negative
    if seed is not None:
        task["seed"] = int(seed)
    res, err = _runware_call(task)
    if err:
        # retry stripped -- some models reject steps/negative/seed. The seed image survives
        # the strip: a required-image model fails without it, and an optional one keeps intent.
        base = {"taskType": "imageInference", "taskUUID": str(uuid.uuid4()),
                "positivePrompt": prompt, "model": air, "width": int(width),
                "height": int(height), "numberResults": 1, "outputType": "URL"}
        if ref:
            base["seedImage"] = ref
        res, err = _runware_call(base)
        if err:
            return None, None, None, err
    url = res.get("imageURL")
    if not url:
        return None, None, None, "no imageURL in response"
    try:
        img = requests.get(url, timeout=60).content
    except Exception as e:
        return None, None, None, "download failed: " + str(e)[:150]
    return img, res.get("seed", seed), res.get("cost"), None


@app.route("/api/models")
def api_models():
    return jsonify(MODELS)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    d = request.get_json(force=True)
    model = MODEL_BY_ID.get(d.get("model"))
    if not model:
        return jsonify({"error": "unknown model '%s'" % d.get("model")}), 400
    prompt = (d.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "empty prompt"}), 400
    negative = d.get("negative") or ""
    width = d.get("width") or 1024
    height = d.get("height") or 1024
    steps = d.get("steps") or model.get("default_steps")
    n = min(int(d.get("n") or 1), 8)
    refs = d.get("refs") or []
    ref = refs[0] if refs else None
    if ref and (model.get("img") or "none") == "none":
        return jsonify({"error": "%s takes no reference image" % model["name"]}), 400

    results, errors = [], []
    for i in range(n):
        seed = d.get("seed")
        if seed is not None:
            seed = int(seed) + i
        img, rseed, rcost, err = runware_generate(model["air"], prompt, negative, width, height, steps, seed, ref)
        if err:
            errors.append(err)
            continue
        iid = "%d_%s" % (int(time.time()), uuid.uuid4().hex[:6])
        slug = _slugify(prompt)
        fname = (slug + "_" + iid + ".png") if slug else (iid + ".png")
        with open(os.path.join(GALLERY, fname), "wb") as f:
            f.write(img)
        rec = {"id": iid, "url": "/gallery/" + fname, "model": model["id"],
               "model_name": model["name"], "provider": model["provider"],
               "seed": rseed, "width": width, "height": height, "steps": steps,
               "prompt": prompt, "negative": negative,
               "ref": (ref if isinstance(ref, str) and not ref.startswith("data:") else ("data-uri" if ref else None)),
               "cost": rcost if rcost is not None else model.get("price", 0),
               "ts": int(time.time())}
        results.append(rec)
        _append_session(rec)

    if not results:
        return jsonify({"error": "generation failed via Runware", "detail": errors[:2]}), 502
    return jsonify({"results": results, "errors": errors})


def _append_session(rec):
    path = os.path.join(STATE, "session.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


@app.route("/api/upload", methods=["POST"])
def api_upload():
    # body: {"image": "data:<mime>;base64,..."} -> Runware imageUpload task -> media UUID.
    d = request.get_json(force=True)
    image = d.get("image") or ""
    if not image.startswith("data:"):
        return jsonify({"error": "expected a data URI"}), 400
    task = {"taskType": "imageUpload", "taskUUID": str(uuid.uuid4()), "image": image}
    res, err = _runware_call(task)
    if err:
        return jsonify({"error": "upload failed via Runware", "detail": err}), 502
    u = res.get("imageUUID")
    if not u:
        return jsonify({"error": "no imageUUID in response"}), 502
    return jsonify({"uuid": u})


@app.route("/api/image/<iid>", methods=["DELETE"])
def api_delete_image(iid):
    # soft delete: the PNG moves to OUTPUT/TRASH (product never gets destroyed outright),
    # the session row drops so the UI forgets it. Two-stage confirm lives client-side.
    path = os.path.join(STATE, "session.jsonl")
    if not os.path.isfile(path):
        return jsonify({"error": "no session log"}), 404
    kept, victim = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("id") == iid:
                victim = r
            else:
                kept.append(line.rstrip("\n"))
    if victim is None:
        return jsonify({"error": "unknown image id"}), 404
    fname = victim["url"].split("/")[-1]
    src = os.path.join(GALLERY, fname)
    trash = os.path.join(GALLERY, "TRASH")
    os.makedirs(trash, exist_ok=True)
    if os.path.isfile(src):
        os.replace(src, os.path.join(trash, fname))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(kept) + ("\n" if kept else ""))
    return jsonify({"ok": True, "trashed": fname})


@app.route("/api/session")
def api_session():
    path = os.path.join(STATE, "session.jsonl")
    if not os.path.isfile(path):
        return jsonify([])
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return jsonify(rows[-60:][::-1])


@app.route("/api/configs", methods=["GET", "POST"])
def api_configs():
    path = os.path.join(STATE, "configs.json")
    if request.method == "POST":
        arr = request.get_json(force=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(arr, f, indent=2)
        return jsonify({"ok": True, "count": len(arr)})
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route("/gallery/<path:fn>")
def gallery(fn):
    return send_from_directory(GALLERY, fn)


@app.route("/")
def index():
    return send_file(os.path.join(STATIC, "index.html"))


@app.route("/<path:fn>")
def static_files(fn):
    return send_from_directory(STATIC, fn)


if __name__ == "__main__":
    runware_key()  # fail fast if the vault gate is dark
    print("unDolphin on http://127.0.0.1:8790  (models: %d)" % len(MODELS))
    app.run(host="127.0.0.1", port=8790, threaded=True)
