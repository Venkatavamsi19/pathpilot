import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class JobAIRecommender:
    def __init__(self, data_folder):
        self.jobs = []
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        for file in os.listdir(data_folder):
            if file.endswith(".json"):
                with open(os.path.join(data_folder, file), "r", encoding="utf-8") as f:
                    data = json.load(f)

                    category = data.get("category", "Unknown")
                    for career in data["careers"]:
                        combined_text = self._build_text(category, career)
                        career["category"] = category
                        career["combined_text"] = combined_text
                        self.jobs.append(career)

        self.embeddings = self.model.encode(
            [job["combined_text"] for job in self.jobs],
            normalize_embeddings=True
        )

    def _build_text(self, category, career):
        skills = career.get("required_skills", {})
        all_skills = sum(skills.values(), [])
        related = career.get("related_skills", [])

        return " ".join([
            category,
            career["name"],
            career["overview"],
            " ".join(all_skills),
            " ".join(related)
        ])

    def recommend(self, query, top_k=5):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = scores.argsort()[-top_k:][::-1]

        results = []
        for i in top_indices:
            job = self.jobs[i]
            job_copy = job.copy()
            job_copy["score"] = round(float(scores[i]), 3)
            results.append(job_copy)

        return results
