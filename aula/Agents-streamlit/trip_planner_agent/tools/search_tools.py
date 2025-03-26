#Importaçãp das bibliotecas necessárias
import json
import requests
import streamlit as st
from langchain.tools import tool

#Criação da classe SearchTools
class SearchTools():

    #Definição da ferramenta search_internet
    #decorada com @tool para registrar a função como uma
    #ferramenta
    @tool("Search the internet")
    def search_internet(query):
        """Útil para pesquisar na internet sobre um
        determinado assunto e retornar resultados relevantes."""
        #Definição de quantos resultados retornar
        top_result_to_return = 4
        #Definição da URL da API
        url = "https://google.serper.dev/search"
        #Preparação do payload, ou seja, a requisição
        #que será enviada para a API
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': st.secrets['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        #Faz a requisição para a API
        response = requests.request("POST", url, headers=headers, data=payload)
        #Verifica se a resposta contém a chave 'organic'
        #que contém os resultados da pesquisa
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        else:
            #Pega os resultados da pesquisa
            results = response.json()['organic']
            string = []
            #Itera sobre os 4 primeiros resultados
            #e os adiciona à string de retorno
            for result in results[:top_result_to_return]:
                try:
                    #Adiciona o título, o link e o snippet de cada resultado
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next
        #Retorna a string formatada com os resultados
        return '\n'.join(string)