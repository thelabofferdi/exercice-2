import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("RODIUMAI_API_KEY")
BASE = "https://api.rodiumai.io/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}",
           "Content-Type": "application/json"}

def etape_chat():
    q = input("Votre question : ")
    r = requests.post(f"{BASE}/chat/completions", headers=HEADERS, json={
        "model": "openai/gpt-4o",
        "messages": [{"role": "user", "content": q}],
    }, timeout=150)
    if r.status_code != 200:
        print("Erreur :", r.status_code, r.json().get("error_code"))
        return
    data = r.json()
    print(data["choices"][0]["message"]["content"])
    print("Coût :", data.get("cost_rodi"), "RODI")

def etape_image():
    desc = input("Décrivez l'image : ")
    r = requests.post(f"{BASE}/images/generations", headers=HEADERS, json={
        "model": "openai/gpt-image-1",
        "prompt": desc,
        "size": "1024x1024",
    }, timeout=150)
    if r.status_code != 200:
        print("Erreur :", r.status_code, r.json().get("error_code"))
        return
    b64 = r.json()["data"][0]["b64_json"]
    with open("image.png", "wb") as f:
        f.write(base64.b64decode(b64))
    print("Image enregistrée : image.png")

def etape_video():
    desc = input("Décrivez la vidéo : ")
    r = requests.post(f"{BASE}/videos/generations", headers=HEADERS, json={
        "model": "google/veo-3.1-generate-preview",
        "prompt": desc,
        "duration_seconds": 4,
    }, timeout=150)
    if r.status_code != 200:
        print("Erreur :", r.status_code, r.json().get("error_code"))
        return
    data = r.json()["data"][0]
    if data.get("b64_json"):
        with open("video.mp4", "wb") as f:
            f.write(base64.b64decode(data["b64_json"]))
    else:
        v = requests.get(data["url"], timeout=150)
        with open("video.mp4", "wb") as f:
            f.write(v.content)
    print("Vidéo enregistrée : video.mp4")

etapes = [("Chat", etape_chat), ("Image", etape_image), ("Vidéo", etape_video)]
i = 0
while True:
    nom, fn = etapes[i]
    print(f"\n=== Étape {i+1} : {nom} ===")
    fn()
    choix = []
    if i > 0:
        choix.append("b) revenir")
    choix.append("r) rester")
    if i < len(etapes) - 1:
        choix.append("s) suivante")
    else:
        choix.append("q) quitter")
    c = input("Choix : " + " / ".join(choix) + " ? ").strip().lower()
    if c == "b" and i > 0:
        i -= 1
    elif c == "s" and i < len(etapes) - 1:
        i += 1
    elif c == "q":
        break
