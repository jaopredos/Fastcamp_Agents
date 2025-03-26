#Importando as bibliotecas necessárias
import json
import requests
import streamlit as st
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

#Criando a classe BrowserTools
class BrowserTools():
    #Definição da função scrape_and_summarize_website 
    #que será utilizada como ferramenta para extrair e resumir o conteúdo de um site
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Útil para extrair e resumir o conteúdo de um site"""
        #Definição da URL da API do Browserless
        url = f"https://chrome.browserless.io/content?token={st.secrets['BROWSERLESS_API_KEY']}"
        #Definição do payload com a URL do site a ser extraído
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        #Requisição POST para a API do Browserless
        response = requests.request("POST", url, headers=headers, data=payload)
        #Processamento do conteúdo extraído
        #Divisão do conteúdo em elementos HTML
        elements = partition_html(text=response.text)
        #Junção dos elementos em uma string
        content = "\n\n".join([str(el) for el in elements])
        #Divisão do conteúdo em chunks de 8000 caracteres
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        #Para cada chunk de conteúdo, cria-se uma tarefa para resumir o conteúdo
        #e o resumo é adicionado à lista de resumos
        for chunk in content:
            #Criação do agente
            agent = Agent(
                #Definição da função do agente
                role='Principal Researcher',
                #Definição do objetivo do agente
                goal='Do amazing researches and summaries based on the content you are working with',
                #Definição da 'identidade' do agente
                #o modo como ele vai se apresentar e se comportar
                backstory="You're a Principal Researcher at a big "
                "company and you need to do a research about a given topic.",
                #O agente não pode delegar tarefas
                allow_delegation=False)
            #Criação da tarefa para resumir o conteúdo do chunk
            task = Task(
                #Definição do agente responsável pela tarefa
                agent=agent,
                #Descrição da tarefa
                description=
                f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )
            #Execução da tarefa
            summary = task.execute()
            #Adição do resumo à lista de resumos
            summaries.append(summary)
        #Retorno dos resumos
        #Os resumos são concatenados em uma única string separada por duas quebras de linha
        return "\n\n".join(summaries)