#Importando as bibliotecas necessárias
import streamlit as st
import requests
import time
from sendmail import send_email  

#Definição da função de pesquisa de jobs
#Essa função irá realizar uma requisição POST para a API
def search_jobs(requirements):
    #Definição dos parâmetros da requisição
    url = 'http://127.0.0.1/research_candidates'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        'job_requirements': f'{requirements}'
    }

    #Realização da requisição
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#Função principal
#Essa função irá criar a interface do Streamlit
def main():
    # nterface Streamlit
    st.title("Pesquisa de Jobs")
    requirements = st.text_input("Digite os requisitos do job:")

    if 'button1_clicked' not in st.session_state:
        st.session_state.button1_clicked = False
    if 'button2_clicked' not in st.session_state:
        st.session_state.button2_clicked = False

    if st.button('Buscar'):
        st.session_state.button1_clicked = True
        st.session_state.button2_clicked = False

    if st.session_state.button1_clicked:
        start_time = time.time()
        with st.spinner("Buscando os melhores candidatos..."):
            #Mostrar animação enquanto carrega
            gif_path = "loading.gif"
            gif_placeholder = st.empty()
            gif_placeholder.image(gif_path)

            #Mostra os resultados da pesquisa
            results = search_jobs(requirements)
            #Finaliza o cronômetro
            end_time = time.time()  
            #Calcula o tempo decorrido
            elapsed_time = end_time - start_time  

            if results:
                #Remove o GIF depois da busca
                gif_placeholder.empty()  
                st.markdown("<h3 style='color:green;'>Busca Finalizada!</h3>", unsafe_allow_html=True)
                st.write("Top 5 Candidatos:")
                #Exibe os resultados
                st.write(f"{results['result']['raw']}")

                #Exibe informações sobre a execução, como tokens usados
                st.write(f"Tokens Usados: {results['result']['token_usage']['total_tokens']}")
                st.write(f"Total de requisições: {results['result']['token_usage']['successful_requests']}")
                st.write(f"Tempo de execução: {elapsed_time:.2f} segundos")
            else:
                st.error("Não foi possível obter resultados.")
    
    #Envio de email com as informações
    email_input = st.text_input("Digite o email do destinatário:", key="email")
    if st.button('Enviar Email'):
        st.session_state.button2_clicked = True
        st.session_state.button1_clicked = False

    if st.session_state.button2_clicked:
        if email_input:
            send_email(email_input, results['result']['raw'])
            st.markdown("<h3 style='color:green;'>Email enviado!</h3>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
