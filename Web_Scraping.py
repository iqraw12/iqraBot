import requests
from bs4 import BeautifulSoup
import re

def search_wikipedia(query, num_sentences=3):
    def clean_html(html):
        soup = BeautifulSoup(html, "html.parser")
        for element in soup(["sup", "table", "style"]):
            element.decompose()
        text = soup.get_text(separator="\n")
        return text

    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srprop": "",
        "utf8": ""
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "query" in data and "search" in data["query"]:
            search_results = data["query"]["search"]
            if search_results:
                page_id = search_results[0]["pageid"]
                params = {
                    "action": "parse",
                    "format": "json",
                    "pageid": page_id,
                    "prop": "text",
                    "section": 0,
                    "utf8": ""
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "parse" in data and "text" in data["parse"]:
                        content_html = data["parse"]["text"]["*"]
                        content_text = clean_html(content_html)
                        
                        # Remove citations and references
                        content_text = re.sub(r"\[\d+\]", "", content_text)
                        
                        # Extract the desired number of sentences
                        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", content_text)
                        shortened_text = ". ".join(sentences[:num_sentences])
                        
                        return shortened_text

    return None

def format_output(content):
    lines = content.split("\n")
    output = ""
    for line in lines:
        line = line.strip()
        if line:
            output += line + "\n"
    return output

def scrape_wikipedia(query):
    result = search_wikipedia(query)
    if result:
        formatted_result = format_output(result)
        return formatted_result
    else:
        return "Failed to retrieve Wikipedia page."