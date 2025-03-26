import requests
import json
import streamlit as st
from unstructured.partition.html import partition_html
from dotenv import load_dotenv
import os

load_dotenv()

BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")

def scrape_website(website: str) -> str:
    url = f"https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)

    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    return content[:8000]  # limitar o tamanho para segurança

browser_tool = {
    "name": "Scrape website content",
    "description": "Scrapes and summarizes the content of a given website",
    "func": scrape_website
}