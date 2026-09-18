# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, subprocess, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en prod : mets ton domaine exact
    allow_methods=["*"],
    allow_headers=["*"],
)

JSON_PATH = "data/actualites.json"

def read_cache():
    if not os.path.exists(JSON_PATH):
        return {"last_update": None, "articles": []}
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/actualites")
def get_actualites():
    return read_cache()

@app.post("/api/actualites/refresh")
def refresh():
    subprocess.run(["python", "scraper.py"], check=True)
    return read_cache()