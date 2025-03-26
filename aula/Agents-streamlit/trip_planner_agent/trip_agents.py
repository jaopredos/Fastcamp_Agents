#Importação das bibliotecas necessárias
from crewai import Agent
import re
import streamlit as st
from langchain_community.llms import OpenAI
from crewai_tools import SerperDevTool

#Mudança no código feita pelo desenvolvedor do projeto original
## My initial parsing code using callback handler to print to app
# def streamlit_callback(step_output):
#     # This function will be called after each step of the agent's execution
#     st.markdown("---")
#     for step in step_output:
#         if isinstance(step, tuple) and len(step) == 2:
#             action, observation = step
#             if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
#                 st.markdown(f"# Action")
#                 st.markdown(f"**Tool:** {action['tool']}")
#                 st.markdown(f"**Tool Input** {action['tool_input']}")
#                 st.markdown(f"**Log:** {action['log']}")
#                 st.markdown(f"**Action:** {action['Action']}")
#                 st.markdown(
#                     f"**Action Input:** ```json\n{action['tool_input']}\n```")
#             elif isinstance(action, str):
#                 st.markdown(f"**Action:** {action}")
#             else:
#                 st.markdown(f"**Action:** {str(action)}")

#             st.markdown(f"**Observation**")
#             if isinstance(observation, str):
#                 observation_lines = observation.split('\n')
#                 for line in observation_lines:
#                     if line.startswith('Title: '):
#                         st.markdown(f"**Title:** {line[7:]}")
#                     elif line.startswith('Link: '):
#                         st.markdown(f"**Link:** {line[6:]}")
#                     elif line.startswith('Snippet: '):
#                         st.markdown(f"**Snippet:** {line[9:]}")
#                     elif line.startswith('-'):
#                         st.markdown(line)
#                     else:
#                         st.markdown(line)
#             else:
#                 st.markdown(str(observation))
#         else:
#             st.markdown(step)

#Mudança feita por mim para o código funcionar
#Definição da ferramenta de busca
search_tool = SerperDevTool()


#Criação da classe TripAgents
#Essa classe é responsável por criar os agentes que serão utilizados no projeto
class TripAgents():
    
    #Método que cria o agente especialista em seleção de cidades
    #Esse agente é responsável por selecionar a melhor cidade com base no clima, estação e preços
    def city_selection_agent(self):
        return Agent(
            #Definição da função/papel do agente
            role='City Selection Expert',
            #Definição do objetivo do agente
            goal='Select the best city based on weather, season, and prices',
            #Definição da "identidade" do agente
            backstory='An expert in analyzing travel data to pick ideal destinations',
            #Definição das ferramentas que o agente irá utilizar
            tools=[
                search_tool,
            ],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True,
            # step_callback=streamlit_callback,
        )

    #Método que cria o agente especialista local
    #Esse agente é responsável por fornecer informações sobre a cidade selecionada
    def local_expert(self):
        return Agent(
            #Definição da função/papel do agente
            role='Local Expert at this city',
            #Definição do objetivo do agente
            goal='Provide the BEST insights about the selected city',
            #Definição da "identidade" do agente
            backstory="""A knowledgeable local guide with extensive information
            about the city, it's attractions and customs""",
            #Definição das ferramentas que o agente irá utilizar
            tools=[
                search_tool
            ],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True,
            # step_callback=streamlit_callback,
        )

    #Método que cria o agente especialista em planejamento de viagens
    #Esse agente é responsável por criar itinerários de viagem com 
    #sugestões de orçamento e embalagem para a cidade
    def travel_concierge(self):
        return Agent(
            #Definição da função/papel do agente
            role='Amazing Travel Concierge',
            #Definição do objetivo do agente
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
            #Definição da "identidade" do agente
            backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
            #Definição das ferramentas que o agente irá utilizar
            tools=[
                search_tool
            ],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True,
            # step_callback=streamlit_callback,
        )

###########################################################################################
# Print agent process to Streamlit app container                                          #
# This portion of the code is adapted from @AbubakrChan; thank you!                       #
# https://github.com/AbubakrChan/crewai-UI-business-product-launch/blob/main/main.py#L210 #
###########################################################################################
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

        if "City Selection Expert" in cleaned_data:
            #Aplica a cor ao texto
            cleaned_data = cleaned_data.replace("City Selection Expert", f":{self.colors[self.color_index]}[City Selection Expert]")
        if "Local Expert at this city" in cleaned_data:
            cleaned_data = cleaned_data.replace("Local Expert at this city", f":{self.colors[self.color_index]}[Local Expert at this city]")
        if "Amazing Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace("Amazing Travel Concierge", f":{self.colors[self.color_index]}[Amazing Travel Concierge]")
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
