from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from semantic_search import get_semantic_recommendations
from feedback_handler import submit_feedback
import json
import os

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

@app.get("/recommendations/")
def get_recommendations(keyword: str):
    key = keyword.lower().strip()
    matched = []

    for level, course_groups in recommendations.items():
        for group_name, course_list in course_groups.items():
            for course in course_list:
                title = course.get("Title", "")
                if key in title.lower():
                    matched.append({title: course})

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
@app.get("/semantic_recommendations/")
def semantic_recommendations(keyword: str):
    return get_semantic_recommendations(
        keyword=keyword,
        recommendations=recommendations,
    )

@app.post("/feedback/")
def post_feedback(user_id: str, course_title: str, rating: float, comment: str = ""):
    if not 1.0 <= rating <= 5.0:
        raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 5.0")
    
    return submit_feedback(user_id, course_title, rating, comment)

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


