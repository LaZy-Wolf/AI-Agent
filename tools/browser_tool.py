def open_url(query: str) -> str:
    # Placeholder for opening a URL (no actual browser automation)
    if "insta" in query.lower() or "instagram" in query.lower():
        return "Opened Instagram: https://www.instagram.com"
    return f"Cannot open URL for query: {query}"