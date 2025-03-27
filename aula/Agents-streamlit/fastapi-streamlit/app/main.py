#Importação das bibliotecas necessárias
import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()

# Definição do servidor FastAPI
app = FastAPI()

# Definição das variáveis de ambiente
serper_key = os.getenv("SERPER_DEV_API_KEY")
if serper_key:
    os.environ["SERPER_DEV_API_KEY"] = serper_key
else:
    print("SERPER_DEV_API_KEY não está definida.")

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
else:
    print("OPENAI_API_KEY não está definida.")

# Define um parâmetro de entrada para a API do tipo string
# Irá conter os requisitos da vaga
class JobRequirements(BaseModel):
    job_requirements: str

# Definição de uma ferramenta de pesquisa que pode ser usado pelo Agente
search_tool = SerperDevTool()
# Definição de um Agente de Recrutamento
researcher = Agent(
    #Definição da função do Agente
    role='Recrutador Senior de Dados',
    #Definição do objetivo do Agente
    goal='Encontrar os melhores perfis de dados para trabalhar baseado nos requisitos da vaga',
    #Parâmetro que define se as mensagens sobre as 
    #ações realizadas pelos agentes serão exibidas
    verbose=True,
    #Parâmetro que define se o Agente irá armazenar em memória
    memory=True,
    #Definição do modelo de linguagem natural que o Agente irá utilizar
    model='gpt-4o-mini',
    #Aqui é definida a "identidade" do agente,
    #ou seja, o modo como ele irá agir
    backstory=(
        'Experiência na área de dados e formação acadêmica em Recursos Humanos e '
        'especialista em LinkedIn, tem domínio das principais táticas de busca de profissionais.'
    ),
    #Definição das ferramentas que o Agente poderá utilizar
    tools=[search_tool]
)

#Definição da rota para a API
#Essa rota irá receber os requisitos da vaga e retornar os candidatos em potencial
@app.post("/research_candidates")
async def research_candidates(req: JobRequirements):
    # Definição de uma tarefa para o Agente
    research_task = Task(
        #Definição da descrição da tarefa
        description=(
            f'Realizar pesquisas completas para encontrar candidatos em potencial para o cargo especificado'
            f'Utilize vários recursos e bancos de dados online para reunir uma lista abrangente de candidatos em potencial.'
            f'Garanta que o candidato atenda os requisitos da vaga. Requisitos da vaga: {req.job_requirements}'
        ),
        #Definição da saída esperada da tarefa
        expected_output="""Uma lista com top 5 candidatos potenciais separada por Bullet points, cada candidato deve
                        conter informações de contato e breve descrição do perfil destacando a sua qualificação para a vaga.
                        Trazer junto a url para encontrar o perfil do candidato.""",
        #Definição da ferramenta que poderá ser utilizada na task
        tools=[search_tool],
        #Definição do Agente responsável pela tarefa
        agent=researcher
    )

    #Criação da equipe que irá executar a tarefa
    crew = Crew(
        #Definição dos agentes que irão compor a equipe
        agents=[researcher],
        #Definição da Tasks que a equipe irá realizar
        tasks=[research_task],
        #Definição do processo de execução da equipe, nessse caso será sequencial
        process=Process.sequential
    )

    #Dando início a execução
    result = crew.kickoff(inputsa={'job_requirements': req.job_requirements})
    #Retornando o resultado
    return {'result': result}

#Rodar o servidor usando o Uvicorn dentro do docker
if __name__ == "__main__":
    import uvicorn
    print('>>>>>>>>>>>>>>>>>>> version V0.0.1')
    uvicorn.run(app, host="0.0.0.0", port=8000)