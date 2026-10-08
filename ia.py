import streamlit as st
from openai import OpenAI

st.write('# chat bot')

# 1. Cria a lista no session_state para salvar o histórico
if 'lista_mensagem' not in st.session_state: 
    st.session_state['lista_mensagem'] = []

# 2. Mostra as mensagens antigas na tela
for mensagem in st.session_state['lista_mensagem']: 
    envia = mensagem['role'] 
    recebe = mensagem['content'] 
    st.chat_message(envia).write(recebe)

# 3. Caixa de texto para o usuário digitar
mensagem_usuario = st.chat_input('Escreva a sua pergunta aqui!')

# 4. Só executa o bloco abaixo se o usuário digitou algo
if mensagem_usuario: 
    # Mostra a mensagem do usuário na tela e salva no histórico
    st.chat_message('user').write(mensagem_usuario) 
    mensagem1 = {'role': 'user', 'content': mensagem_usuario} 
    st.session_state['lista_mensagem'].append(mensagem1)

    # Configura a IA (Agora DENTRO do if com espaços na esquerda)
    cabeca_ia = OpenAI(
        api_key=st.secrets['GEMINI_API_KEY'],
        base_url='https://generativelanguage.googleapis.com/v1beta/openai'
    )

    # Faz a chamada para o Gemini passando o histórico atualizado
    resposta_cabeça = cabeca_ia.chat.completions.create( 
        messages=st.session_state['lista_mensagem'], 
        model='gemini-flash-lite-latest'
    )

    # Pega o texto da resposta da IA
    resposta_ia = resposta_cabeça.choices[0].message.content

    # Mostra a resposta da IA na tela e salva no histórico
    st.chat_message('assistant').write(resposta_ia) 
    mensagem2 = {'role': 'assistant', 'content': resposta_ia} 
    st.session_state['lista_mensagem'].append(mensagem2)