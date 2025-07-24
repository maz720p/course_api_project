from sentence_transformers import SentenceTransformer, util
import torch

# Load SBERT model sekali saja
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_recommendations(
    keyword: str,
    recommendations: dict,
    threshold: float = 0.5,
    min_results: int = 15,
    top_k: int = 500
):
    all_courses = {}

    # Gabungkan semua kursus dari semua level
    for level, course_groups in recommendations.items():
        for group_name, course_list in course_groups.items():
            for course in course_list:
                title = course.get("Title", "")
                if title:
                    all_courses[title] = {
                        "info": course,
                        "level": level.replace("_Course", "")
                    }

    course_titles = list(all_courses.keys())

    # Encode keyword dan semua judul kursus
    keyword_embedding = model.encode(keyword, convert_to_tensor=True)
    title_embeddings = model.encode(course_titles, convert_to_tensor=True)

    # Hitung cosine similarity
    cosine_scores = util.cos_sim(keyword_embedding, title_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(top_k, len(course_titles)))

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        similarity = score.item()
        if similarity < threshold:
            continue
        title = course_titles[idx]
        course_info = all_courses[title]["info"]
        level = all_courses[title]["level"]
        results.append({
            "title": title,
            "score": round(similarity, 4),
            "level": level,
            "info": course_info
        })

    # Jika hasil terlalu sedikit, turunkan threshold
    if len(results) < min_results and threshold > 0.35:
        return get_semantic_recommendations(
            keyword,
            recommendations,
            threshold=threshold - 0.05,
            min_results=min_results,
            top_k=top_k
        )

    return {
        "status": "success",
        "keyword": keyword,
        "results": results
    }
