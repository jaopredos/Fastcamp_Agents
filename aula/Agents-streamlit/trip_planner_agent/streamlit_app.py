#Importação das bibliotecas necessárias
from crewai import Crew
from trip_agents import TripAgents, StreamToExpander
from trip_tasks import TripTasks
import streamlit as st
import datetime
import sys

# Ignorar avisos de depreciação e avisos de usuário
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# Configuração da página
st.set_page_config(page_icon="✈️", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

#Definição da classe TripCrew, responsável por criar a 'ideia' de uma viagem
class TripCrew:

    #Definição do método construtor da classe
    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.output_placeholder = st.empty()

    #Definição do método run, responsável por executar a equipe de agentes
    #que irá planejar a viagem
    def run(self):
        #Puxa as classes TripAgents e TripTasks
        agents = TripAgents()
        tasks = TripTasks()

        #Criação dos agentes da tarefa
        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        #Definição da tarefa de identificação
        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        #Definição da tarefa de coleta de informações sobre a cidade
        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        #Definição da tarefa de planejamento da viagem
        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        #Criação da equipe de agentes
        crew = Crew(
            #Definição dos agentes
            agents=[
                city_selector_agent, local_expert_agent, travel_concierge_agent
            ],
            #Definição das tarefas
            tasks=[identify_task, gather_task, plan_task],
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

    #Definição do ícone da página
    icon("🏖️ VacAIgent")

    #Definição de um subtítulo 
    st.subheader("Let AI agents plan your next vacation!",
                 divider="rainbow", anchor=False)

    import datetime

    #Definição da data atual para marcar a viagem
    today = datetime.datetime.now().date()
    #Definição da data de 10 de janeiro do próximo ano como data
    #final para marcar a viagem (padrão)
    next_year = today.year + 1
    jan_16_next_year = datetime.date(next_year, 1, 10)
    
    #Definição de uma barra lateral
    with st.sidebar:
        st.header("👇 Enter your trip details")
        #Definição de um formulário para coletar informações
        #sobre a viagem
        with st.form("my_form"):
            #Definição dos campos do formulário
            #Campo para a localização atual do usuário
            location = st.text_input(
                "Where are you currently located?", placeholder="San Mateo, CA")
            #Campo para a cidade e país que o usuário deseja visitar
            cities = st.text_input(
                "City and country are you interested in vacationing at?", placeholder="Bali, Indonesia")
            #Campo para o intervalo de datas em que o usuário deseja viajar
            date_range = st.date_input(
                "Date range you are interested in traveling?",
                min_value=today,
                value=(today, jan_16_next_year + datetime.timedelta(days=6)),
                format="MM/DD/YYYY",
            )
            #Campo para os interesses e hobbies do usuário
            #ou detalhes extras sobre a viagem
            interests = st.text_area("High level interests and hobbies or extra details about your trip?",
                                     placeholder="2 adults who love swimming, dancing, hiking, and eating")

            #Botão de envio do formulário
            submitted = st.form_submit_button("Submit")

        st.divider()

        #Parte do código que dá créditos ao criador do projeto
        # Credits to joaomdmoura/CrewAI for the code: https://github.com/joaomdmoura/crewAI
        st.sidebar.markdown(
        """
        Credits to [**@joaomdmoura**](https://twitter.com/joaomdmoura)
        for creating **crewAI** 🚀
        """,
            unsafe_allow_html=True
        )

        st.sidebar.info("Click the logo to visit GitHub repo", icon="👇")
        st.sidebar.markdown(
            """
        <a href="https://github.com/joaomdmoura/crewAI" target="_blank">
            <img src="https://raw.githubusercontent.com/joaomdmoura/crewAI/main/docs/crewai_logo.png" alt="CrewAI Logo" style="width:100px;"/>
        </a>
        """,
            unsafe_allow_html=True
        )


#Verifica se o formulário foi enviado
if submitted:
    #Criação de uma barra de status para mostrar o progresso
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        #Criação de um contêiner para mostrar o resultado
        with st.container(height=500, border=False):
            #Redireciona o print do console para o contêiner
            #da aplicação
            sys.stdout = StreamToExpander(st)
            #Criação de uma instância da classe TripCrew
            #para planejar a viagem
            trip_crew = TripCrew(location, cities, date_range, interests)
            #Executa a função responsável por acionar os agentes
            #e planejar a viagem
            result = trip_crew.run()
        #Atualiza o status da barra de status
        status.update(label="✅ Trip Plan Ready!",
                      state="complete", expanded=False)

    #Exibe o resultado da execução da equipe de agentes
    st.subheader("Here is your Trip Plan", anchor=False, divider="rainbow")
    st.markdown(result)
