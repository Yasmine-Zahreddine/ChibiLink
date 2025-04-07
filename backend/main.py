from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from backend import database
from datetime import datetime, timezone
from backend import security
from backend import logger

app = FastAPI()
rate_limiter = security.RateLimiter(max_requests=5, window=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Move the template to a separate string with proper escaping
ERROR_PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ChibiLink - Error</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            min-height: 100vh;
            box-sizing: border-box;
        }}
        .error-container {{
            max-width: 600px;
            min-width: 280px;
            width: 90%;
            margin-top: 200px;
            text-align: center;
            padding: 30px 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #f25278;
            margin-top: 0;
            font-size: 24px; }}
        p {{color: #666;
            margin: 15px 0;
            font-size: 16px;
            line-height: 1.5;}}
        
    </style>
</head>
<body>
    <div class="error-container">
        <h1>{title}</h1>
        <p>{message}</p>
    </div>
</body>
</html>
'''

@app.post("/shorten")
async def create_short_url(request: Request):
    await rate_limiter.check_rate_limit(request)
    data = await request.json()
    url = data.get("url")
    expiration_date = data.get("expiration_date")
    one_time_click = data.get("one_time_click", False)
    length = data.get("length", 6)
    if not security.protect_against_spam(url):
        raise HTTPException(
            status_code=402,
            detail="URL blocked due to suspicious content"
        )
    base_url = request.base_url
    short_url = database.get_shortened_url(url=url, base_url=base_url, expiration_date=expiration_date, one_time_click=one_time_click, length=length)
    if not short_url:
        return {"error": "Invalid URL"}
    return {"new_url": short_url}


@app.api_route("/{short_code}", methods=['GET', 'POST'])
def redirect_to_original_url(short_code: str):
    # Ignore favicon requests
    if short_code == 'favicon.ico':
        return HTMLResponse(
            content="Not Found",
            status_code=404
        )
        
    url_obj = database.get_original_url(short_code=short_code)
    
    # Handle non-existent URLs
    if not url_obj:
        return HTMLResponse(
            content=ERROR_PAGE_TEMPLATE.format(
                title="Link Not Found",
                message="The requested short link does not exist."
            ),
            status_code=404
        )
    
    # Handle expired URLs
    if url_obj.expiration_date < datetime.now(timezone.utc):
        database.delete_url_entry(url_pk=url_obj.url_pk)
        return HTMLResponse(
            content=ERROR_PAGE_TEMPLATE.format(
                title="Link Expired",
                message="This link has expired and is no longer available."
            ),
            status_code=410
        )
    
    # Handle one-time use links
    if url_obj.one_time_click and url_obj.clicks > 0:
        database.delete_url_entry(url_pk=url_obj.url_pk)
        return HTMLResponse(
            content=ERROR_PAGE_TEMPLATE.format(
                title="Link Expired",
                message="This was a one-time link and has already been used."
            ),
            status_code=410
        )
    
    # Handle successful redirects
    url_obj = database.add_url_click(url_obj.url_pk)
    return RedirectResponse(url_obj.original_url, status_code=307)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)