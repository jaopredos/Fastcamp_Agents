#Importação da biblioteca necessária
from langchain.tools import tool

#Criação da classe CalculatorTools
class CalculatorTools():

    #Definição da ferramenta calculate
    #decorada com @tool para registrar a função como uma
    #ferramenta
    @tool("Make a calcualtion")
    def calculate(operation):
        """Útil para realizar qualquer cálculo matemático, 
        como soma, subtração, multiplicação, divisão, etc.
        A entrada para essa ferramenta deve ser uma expressão
        matemática — alguns exemplos são 200*7 ou 5000/2*10.
        """
        return eval(operation)