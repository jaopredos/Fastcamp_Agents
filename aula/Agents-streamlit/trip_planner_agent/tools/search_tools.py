import requests
import json
import streamlit as st

def search_internet(query: str) -> str:
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': st.secrets['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()

    if 'organic' not in data:
        return "Sorry, I couldn't find anything."

    results = data['organic']
    return '\n'.join([
        f"Title: {r['title']}\nLink: {r['link']}\nSnippet: {r['snippet']}\n-----------------"
        for r in results[:4]
    ])

search_tool = {
    "name": "Search the internet",
    "description": "Searches the internet about a topic and returns relevant results",
    "func": search_internet
}