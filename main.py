from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Aktifkan CORS agar bisa diakses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # batasi ke domain frontend jika di produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data JSON saat startup
with open("recommendations_all_combinations.json", "r", encoding="utf-8") as f:
    recommendations = json.load(f)

@app.on_event("startup")
async def startup_event():
    print("\n FastAPI server is running!")
    print(" Docs: http://localhost:8000/docs")
    print(" Try example: http://localhost:8000/recommendations/?keyword=python data\n")

@app.get("/")
def root():
    return {"message": "Welcome to the Course Recommendation API"}

@app.get("/recommendations/")
def get_recommendations(keyword: str):
    key = keyword.lower().strip()
    matched = []

    for k, v in recommendations.get("Beginner_Course", {}).items():
        if key in k.lower():
            matched.append({k: v})

    if matched:
        return {
            "status": "success",
            "keyword": key,
            "data": matched
        }
    else:
        return {
            "status": "error",
            "message": f"No results found for '{key}'"
        }