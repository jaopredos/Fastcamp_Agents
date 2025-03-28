#Importação das bibliotecas necessárias
from crewai import Task, Process
from textwrap import dedent

#Criação das tasks que serão utilizadas no projeto
class ActivityTasks():
    
    #Definição da tarefa de busca de informações
    def search_task(self, subject, agent):
        return Task(
            #Definição da tarefa de busca de informações
            description=dedent(f""""
            Conduct an extensive search on the topic of {subject}.
            Gather plenty of information so that seven distinct questions 
            can be created about this theme.             
            """),
            #Definição da saída esperada
            expected_output="A file containing this information will be used to create the questions for the activity list.",
            #Definição do agente que irá realizar a tarefa
            agent=agent,
            #Definição do processo que o agente irá utilizar para realizar a tarefa
            #Nesse caso, o agente irá realizar a tarefa de forma sequencial
            process = Process.sequential
        )
    
    #Definição da tarefa de criação de questões
    def question_task(self, agent):
        return Task(
            #Definição da tarefa de criação de questões
            description=dedent(f"""
            Create seven distinct questions in the format of multiple-choice items,
            with options from a to e, based on the information provided by the other agent.
            The questions should be clear, concise, and relevant to the topic.
            """),
            #Definição da saída esperada
            expected_output="A list of seven multiple-choice questions with the answers at the end.",
            #Definição do agente que irá realizar a tarefa
            agent=agent
        )