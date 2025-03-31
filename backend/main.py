from fastapi import FastAPI, Request
import models
from fastapi.responses import RedirectResponse
import database
from datetime import datetime, timezone

app = FastAPI()


@app.post("/shorten")
async def create_short_url(request: Request):
    data = await request.json()
    url = data.get("url")
    expiration_date = data.get("expiration_date")
    one_time_click = data.get("one_time_click", False)
    length = data.get("length", 6)
    base_url = request.base_url
    short_url = database.get_shortened_url(url=url, base_url=base_url, expiration_date=expiration_date, one_time_click=one_time_click, length=length)
    return {"new_url": short_url}


@app.api_route("/{short_code}", methods=['GET', 'POST'])
def redirect_to_original_url(short_code: str):
    url_obj = database.get_original_url(short_code=short_code)
    if not url_obj:
        return{"error": 'URL not found'}
    if url_obj.expiration_date < datetime.now(timezone.utc):
        database.delete_url_entry(url_pk=url_obj.url_pk)
        return {"error": 'URL expired'}
    if url_obj.one_time_click and url_obj.clicks > 0:
        database.delete_url_entry(url_pk=url_obj.url_pk)
        return {"error": 'URL expired'}
    url_obj = database.add_url_click(url_obj.url_pk)
    return RedirectResponse(url_obj.original_url, status_code=307)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)