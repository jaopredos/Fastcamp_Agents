#Importação das bibliotecas necessárias
from crewai import Crew
from agents import TestAgents, StreamToExpander
from tasks import ActivityTasks
import re
import streamlit as st
import datetime
import sys
from dotenv import load_dotenv
import os

#Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

#Definição da chave da API do SerperDev e OpenAI
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_DEV_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Ignorar avisos de depreciação e avisos de usuário
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


#Definição da classe TripCrew, responsável por criar a 'ideia' de uma viagem
class TripCrew:

    #Definição do método construtor da classe
    def __init__(self, subject):
        self.subject = subject
        self.output_placeholder = st.empty()

    #Definição do método run, responsável por executar a equipe de agentes
    #que irá planejar a viagem
    def run(self):
        #Puxa as classes TripAgents e TripTasks
        agents = TestAgents()
        tasks = ActivityTasks()

        #Criação dos agentes da tarefa
        searcher_agent = agents.search_agent()
        teacher_agent = agents.teacher_agent()

        #Definição da tarefa de pesquisa e obtenção de informações
        search_task = tasks.search_task(
            self.subject,
            searcher_agent,
        )

        #Definição da tarefa de criação de questões
        #Essa tarefa utiliza a informação obtida na tarefa de pesquisa
        question_task = tasks.question_task(
            teacher_agent,
        )

        #Criação da equipe de agentes
        crew = Crew(
            #Definição dos agentes
            agents=[
                searcher_agent,teacher_agent
            ],
            #Definição das tarefas
            tasks=[search_task, question_task],
            #Parâmetro que define se as mensagens sobre as 
            #ações realizadas pelos agentes serão exibidas
            verbose=True
        )

        #Execução da equipe de agentes
        result = crew.kickoff()
        #Salva o resultado da execução da equipe de agentes
        #nessa variável
        self.output_placeholder.markdown(result)

        #Retorna o resultado da execução da equipe de agentes
        return result


#Criação da UI da aplicação
if __name__ == "__main__":
    #Definição do título da aplicação
    st.title("🧠 AI Generator of Educational Questions")

    #Instruções para o usuário
    st.markdown("Insira abaixo o **tema** sobre o qual você deseja gerar questões.", unsafe_allow_html=True)

    #Espaço para o tema no centro da tela
    subject = st.text_area(
        "Tema das questões:",
        placeholder="Ex: Revolução Francesa, Cálculo diferencial, Fotossíntese...",
        height=150
    )

    #Definição do botão para gerar as questões
    submitted = st.button("Gerar questões")

    #Verifica se o botão foi pressionado e se o tema não está vazio
    if submitted and subject.strip() != "":
        #Exibe o status de execução
        with st.status("🤖 **Agentes trabalhando...**", state="running", expanded=True) as status:
            #Container do Streamlit para a saída formatada
            with st.container(height=500, border=False):
                #Redireciona a saída para o app
                sys.stdout = StreamToExpander(st)
                #Criação e executação dos agentes
                trip_crew = TripCrew(subject)
                result = trip_crew.run()
            #Atualiza status para indicar que a execução foi concluída
            status.update(label="✅ Questões geradas com sucesso!", state="complete", expanded=False)

        #Mostra o resultado final
        st.subheader("📝 Questões geradas", anchor=False, divider="rainbow")
        st.markdown(result)

    #Se o botão foi pressionado e o tema está vazio, exibe um aviso
    elif submitted:
        st.warning("⚠️ Por favor, insira um tema antes de prosseguir.")
