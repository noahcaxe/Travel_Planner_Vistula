import httpx

AIC_BASE = "https://api.artic.edu/api/v1"
FIELDS = "id,title,artist_display,image_id"
IIIF_URL = "https://www.artic.edu/iiif/2"

async def fetch_artwork(artwork_id: int) -> dict | None:
    url = f"{AIC_BASE}/artworks/{artwork_id}?fields={FIELDS}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()["data"]
        image_id = data.get("image_id")
        return {
            "title": data["title"],
            "artist": data.get("artist_display"),
            "image_url": f"{IIIF_URL}/{image_id}/full/843,/0/default.jpg" if image_id else None,
        }