#Importando as bibliotecas necessárias
import requests
import json

#Definição dos parâmetros da requisição
url = 'http://localhost:8000/research_candidates'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "job_requirements": "Experiência com Python, SQL e Machine Learning"
}

#Realização da requisição
response = requests.post(url, headers=headers, json=data)

#Exibição do resultado da requisição
print(f'Status Code: {response.status_code}')
print(f'Response JSON:')
print(json.dumps(response.json(), indent=4, ensure_ascii=False))