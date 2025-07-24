
# Course Recommendation REST API  
Final Project – FastAPI-Based Semantic and Keyword Course Recommendation System  
by **Amelia Hari Fauziah** and **Mamluatul 'Azazah**  
Group 6 ML Ops – SISTECH 2025  

A course recommendation system built as a lightweight RESTful API using **FastAPI**. It supports:  
- **Literal keyword-based search**  
- **Semantic search** using the `all-MiniLM-L6-v2` model  
- **Feedback collection** via a dedicated endpoint  

All endpoints are documented through **Swagger UI** and ready for frontend consumption.

---

## Features Implemented

- Lightweight REST API using **FastAPI**  
- Integrated with **Swagger UI** for testing and documentation  
- Semantic search via Sentence Transformers (`all-MiniLM-L6-v2`)  
- Feedback collection through the `/feedback/` endpoint  
- Literal keyword matching via `/recommendations/`  
- Automatic embedding and similarity scoring  
- JSON-based data for fast access and easy updates

---

## Project Structure

```
course_api_project/
├── main.py                             # Main FastAPI app
├── semantic_search.py                  # Semantic search implementation
├── feedback_handler.py                 # Feedback saving logic
├── recommendations_all_combinations.json  # Preprocessed course dataset
├── requirements.txt                    # Python dependencies
├── feedback.json                       # Feedback data
└── README.md                           # This documentation
```

---

## Tech Stack

- Python 3  
- FastAPI  
- Uvicorn  
- Sentence Transformers (`all-MiniLM-L6-v2`)  
- PyTorch  
- JSON  

---

## Cloning and Running Locally

1. **Clone the repository**:
```bash
git clone https://github.com/maz720p/course_api_project.git
cd course_api_project
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the FastAPI server**:
```bash
uvicorn main:app --reload
```

4. **Open in browser**:  
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints Overview

### `GET /recommendations/?keyword=...`  
Returns matching courses that contain the keyword in their titles.

**Example**:  
`http://localhost:8000/recommendations/?keyword=python`

---

### `GET /semantic_recommendations/?keyword=...`  
Returns semantically similar course recommendations based on query meaning.

**Example**:  
`http://localhost:8000/semantic_recommendations/?keyword=python data`

---

### `POST /feedback/`  
Saves user feedback with JSON payload.

**Payload Example**:
```json
{
  "user_id": "user123",
  "course_title": "Python for Beginners",
  "rating": 5,
  "comment": "Very helpful course!"
}
```

---

## Workflow Overview

### 1. Startup Initialization
- Loads the preprocessed dataset from `recommendations_all_combinations.json` once on startup.
- Loads the `SentenceTransformer` model (`all-MiniLM-L6-v2`) for semantic search once into memory.

### 2. Keyword-Based Search (`/recommendations/`)
- Performs case-insensitive substring matching between the user query and course titles.
- Returns all matching courses that contain the keyword in their title.

### 3. Semantic Search (`/semantic_recommendations/`)
- The user’s query is encoded into a dense vector using `SentenceTransformer`.
- All course titles are embedded and compared using cosine similarity.
- Results with similarity above a defined threshold (default: 0.5) are returned.
- If too few results are found, the threshold will gradually lower (until `min_results` is satisfied).
- This allows support for related concepts, e.g., searching "AI" still matches "Artificial Intelligence".

### 4. Feedback Submission (`/feedback/`)
- Accepts a POST request with:
  - `user_id` (string)
  - `course_title` (string)
  - `rating` (float between 1.0 and 5.0)
  - `comment` (optional)
- Prevents duplicate feedback per user per course.
- Stores the feedback in `feedback.json` with a timestamp for audit tracking.

---

## Results Example

```json
{
  "status": "success",
  "keyword": "ML",
  "results": [
    {
      "title": "Machine Learning",
      "score": 0.7541,
      "level": "Intermediate_Professional Certificate",
      "info": {
        "Title": "Machine Learning",
        "Rating": 4.9,
        "Reviews": "4.9K reviews",
        "Level": "Intermediate",
        "Duration": "1 - 3 Months",
        "Certificate_Type": "Professional Certificate",
        "weighted_score": 0.00003882399590473196
      }
    }
  ]
}
```

---

## Why Use Sentence Transformers?

Unlike traditional keyword search, Sentence Transformers can:

- Understand the meaning behind the user's input  
- Match semantically similar phrases (e.g., "AI" ≈ "Artificial Intelligence")  
- Deliver more relevant recommendations, even when keywords do not exactly match  

Model used: `all-MiniLM-L6-v2`  
- Lightweight  
- Fast enough for real-time use  
- Pretrained on large text corpora for general-purpose understanding  

---

## Limitations

- Feedback is stored but not analyzed (future use)  

---

## Future Work

- Analyze feedback to improve scoring  
- Add collaborative filtering for personalization  
- Build a frontend with Streamlit or React  

---

## Contact

Made by **Amelia Hari Fauziah** and **Mamluatul 'Azazah**  
Final Project – MLOps Group 6 – SISTECH 2025  

Feel free to connect for questions, improvements, or collaboration.
