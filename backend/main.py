
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "6e7b2b65"

@app.get("/movie-info")
def get_movie_info(title: str = Query(..., description="Movie title")):
    search_url = f"https://api.themoviedb.org/3/search/movie"
    search_params = {"api_key": TMDB_API_KEY, "query": title}
    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()

    if not search_data["results"]:
        return {"error": "فیلمی با این عنوان یافت نشد."}

    movie = search_data["results"][0]
    movie_id = movie["id"]

    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    details_params = {"api_key": TMDB_API_KEY}
    details_response = requests.get(details_url, params=details_params)
    details_data = details_response.json()

    similar_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
    similar_params = {"api_key": TMDB_API_KEY}
    similar_response = requests.get(similar_url, params=similar_params)
    similar_data = similar_response.json()

    result = {
        "title": details_data.get("title"),
        "genres": [genre["name"] for genre in details_data.get("genres", [])],
        "overview": details_data.get("overview"),
        "poster_path": f"https://image.tmdb.org/t/p/w500{details_data.get('poster_path')}" if details_data.get("poster_path") else None,
        "similar": [
            {
                "title": sim.get("title"),
                "poster_path": f"https://image.tmdb.org/t/p/w200{sim.get('poster_path')}" if sim.get("poster_path") else None
            }
            for sim in similar_data.get("results", [])[:5]
        ]
    }

    return result
