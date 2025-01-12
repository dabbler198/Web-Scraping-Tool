from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from scraper import Scraper

app = FastAPI()

scrape_tool = Scraper()

# static token for authentication
STATIC_TOKEN = "mysecrettoken"

# Validating the token
async def authenticate(x_token: str = Header(...)):
    if x_token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")

@app.get("/get-scraped-data")
async def get_scraped_data(n: int | None = None, alias: str | None = None, token: str = Depends(authenticate)) -> str:
    number_of_pages_to_scrape = 1 if n is None else n
    return scrape_tool.scrape_data(number_of_pages_to_scrape, alias)
