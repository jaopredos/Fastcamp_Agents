#Importação das bibliotecas necessárias
import streamlit as st

from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI

#Definição do modelo de linguagem natural que será utilizado
llm = ChatOpenAI()

#Definição de imagens para os avatares dos agentes
avators = {"Writer":"https://cdn-icons-png.flaticon.com/512/320/320336.png",
            "Reviewer":"https://cdn-icons-png.freepik.com/512/9408/9408201.png"}


#Definição da classe que irá tratar os callbacks
#ela exibe as interações no chat
#e adiciona as mensagens na sessão
class MyCustomHandler(BaseCallbackHandler):

    #Definição do construtor da classe
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    #Definição da função que será chamada quando a cadeia de execução começar
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        #Adicionando a mensagem na sessão e exibindo no
        #chat, com o nome do Agente e o avatar correspondente
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])
    
    #Definição da função que será chamada quando a cadeia de execução terminar
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        #Adicionando a mensagem na sessão e exibindo no
        #chat, com o nome do Agente e o avatar correspondente
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name, avatar=avators[self.agent_name]).write(outputs['output'])

#Definição do Agente
writer = Agent(
    #Definição da função do Agente
    role='Blog Post Writer',
    #Aqui é definida a "identidade" do agente,
    #ou seja, o modo como ele irá agir
    backstory='''You are a blog post writer who is capable of writing a travel blog.
                      You generate one iteration of an article once at a time.
                      You never provide review comments.
                      You are open to reviewer's comments and willing to iterate its article based on these comments.
                      ''',
    #Definição do objetivo do Agente
    goal="Write and iterate a decent blog post.",
    #Opcional definir as tools como lista vazia, pois já
    #é o valor padrão
    # tools=[]  
    #Definição do modelo de linguagem natural que o Agente irá utilizar
    llm=llm,
    #Definição do callback que será chamado quando a cadeia de execução começ
    callbacks=[MyCustomHandler("Writer")],
)

#Definição do Agente
reviewer = Agent(
    #Definição da função do Agente
    role='Blog Post Reviewer',
    #Aqui é definida a "identidade" do agente,
    #ou seja, o modo como ele irá agir
    backstory='''You are a professional article reviewer and very helpful for improving articles.
                 You review articles and give change recommendations to make the article more aligned with user requests.
                 You will give review comments upon reading entire article, so you will not generate anything when the article is not completely delivered. 
                 You never generate blogs by itself.''',
    #Definição do objetivo do Agente
    goal="list builtins about what need to be improved of a specific blog post. Do not give comments on a summary or abstract of an article",
    #Opcional definir as tools como lista vazia, pois já
    #é o valor padrão
    # tools=[]  
    #Definição do modelo de linguagem natural que o Agente irá utilizar
    llm=llm,
    #Definição do callback que será chamado quando a cadeia de execução começar e terminar
    callbacks=[MyCustomHandler("Reviewer")],
)

#Definição do título da página
st.title("💬 CrewAI Writing Studio") 

#Verificando se a sessão já foi iniciada,
#caso não tenha sido, será criada uma lista com uma mensagem inicial
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What blog post do you want us to write?"}]

#Exibindo as mensagens
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#Definição do campo de entrada de texto
#para o usuário inserir o prompt
if prompt := st.chat_input():

    #Salva a mensagem na sessão e exibe no
    #chat, com o usuário e o que ele digitou
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    #Definição da tarefa
    task1 = Task(
        #Definição da descrição da tarefa
        description=f"""Write a blog post of {prompt}. """,
        #Definição de quem será o Agente responsável pela tarefa
        agent=writer,
        #Definição da saída esperada da tarefa
        expected_output="an article under 300 words."
    )

    #Definição da tarefa
    task2 = Task(
        #Definição da descrição da tarefa
        description="""list review comments for improvement from the entire content of blog post to make it more viral on social media""",
        #Definição de quem será o Agente responsável pela tarefa
        agent=reviewer,
        #Definição da saída esperada
        expected_output="Builtin points about where need to be improved."
    )

    #Definição do Crew, a equipe que irá realizar as tarefas
    project_crew = Crew(
        #Definição das tarefas que a equipe irá realizar
        tasks=[task1, task2], 
        #Definição dos agentes que irão compor a equipe 
        agents=[writer, reviewer],
        #Definição do modelo de linguagem natural que a equipe irá utilizar
        manager_llm=llm,
        #Definição do processo de execução da equipe, nesse caso será hierárquico,
        #ou seja, o resultado da primeira tarefa será a entrada da segunda tarefa
        process=Process.hierarchical  
    )
    #Dando início a execução da equipe
    final = project_crew.kickoff()

    #Exibindo o resultado final
    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)