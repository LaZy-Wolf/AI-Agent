from youtube_search import YoutubeSearch

def youtube_search(query: str) -> str:
    try:
        results = YoutubeSearch(query.replace("search for", "").strip(), max_results=1).to_dict()
        if results:
            video = results[0]
            return f"Video: {video['title']} - https://www.youtube.com/watch?v={video['id']}"
        return "No YouTube video found."
    except Exception as e:
        return f"Error searching YouTube: {str(e)}" 