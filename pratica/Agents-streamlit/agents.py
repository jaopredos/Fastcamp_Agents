#Importação das bibliotecas necessárias
from crewai import Agent
import streamlit as st
from crewai_tools import SerperDevTool
import re

#Definição da ferramenta de busca
search_tool = SerperDevTool()

#Criação da classe dos Agentes que serão utilizados no projeto
class TestAgents():

    #Método que cria o agente que é especialista em fazer buscas na internet
    #Este agente é responsável por buscar informações sobre o assunto solicitado
    def search_agent(self):
        return Agent(
            #Definição da função/papel do agente
            role='Search Expert',
            #Definição do objetivo do agente
            goal='Search for information about the subject requested',
            #Definição da "identidade" do agente
            backstory='An expert in searching for information about the subject requested',
            #Definição das ferramentas que o agente irá utilizar
            tools=[
                search_tool,
            ],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True,
            #Esse agente não pode delegar tarefas para outros agentes
            allow_delegation=False
        )
    
    #Método que cria o agente especialista em desenvolver questões sobre o assunto especificado
    #Esse agente é responsável por desenvolver questões sobre o assunto especificado para os alunos
    def teacher_agent(self):
        return Agent(
            #Definição da função/papel do agente
            role='Teacher Expert',
            #Definição do objetivo do agente
            goal='Create questions about the subject specified',
            #Definição da "identidade" do agente
            backstory='An expert in creating questions about the subject specified',
            #Definição das ferramentas que o agente irá utilizar
            tools=[
                search_tool,
            ],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True,
        )
    
#Definição da classe StreamToExpander
#Essa classe é responsável por exibir as mensagens dos agentes no app
class StreamToExpander:
    #Definição do método construtor da classe
    def __init__(self, expander):
        #Componente visual que irá exibir as mensagens
        self.expander = expander
        #Lista que irá armazenar as mensagens
        self.buffer = []
        #Lista de cores
        self.colors = ['red', 'green', 'blue', 'orange']  
        #Índice da cor
        self.color_index = 0 


    def write(self, data):
        #Retira os códigos ANSI para que eles não sejam exibidos no app
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        #Tenta extrair o valor da chave "task" do JSON
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        #Caso o valor da chave "task" exista, exibe uma mensagem no app
        if task_value:
            st.toast(":robot_face: " + task_value)

        #Verifica se a mensagem contém a string "Entering new CrewAgentExecutor chain"
        #Caso contenha, aplica uma cor diferente e muda o índice da cor
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors)  
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Search Expert" in cleaned_data:
            #Aplica a cor ao texto
            cleaned_data = cleaned_data.replace("Search Expert", f":{self.colors[self.color_index]}[Search Expert]")
        if "Teacher Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("Teacher Expert", f":{self.colors[self.color_index]}[Teacher Expert]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        #Adiciona a mensagem na lista de mensagens
        self.buffer.append(cleaned_data)
        #Verifica se a mensagem contém a quebra de linha
        if "\n" in data:
            #Exibe a mensagem no app
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

    #Necessário para compatibilidade com sys.stdout
    def flush(self):
        pass  
