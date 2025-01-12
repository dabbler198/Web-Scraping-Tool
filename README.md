# Web-Scraping-Tool
This tool is designed using FastAPI framework in Python to scrape data from the website: https://dentalstall.com/shop/

The api endpoint can take two optional input parameters:

  n: represents the integer value number of pages to scrape. default value is set to 1
  
  alias: represents proxy url string that can be used to access the target website. default value is None

The endpoint also expects mandatory authentication key via request headers.
