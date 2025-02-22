




def function(memory):    
    # Cargar el prompt JSON
    prompt = prompt_s3()

    # Configurar modelo LangChain
    chat = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Crear mensaje con los datos del JSON
    messages = [
        SystemMessage(content=prompt["role"] + " " + prompt["instructions"] + " " + prompt["context"]),
        HumanMessage(content="Explica el proceso de extracción de litio")
    ]





    # Inicializar el modelo
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    conversation = ConversationChain(llm=llm, memory=memory)

    # Generar respuesta con memoria
    response = conversation.predict(input=message)









sentences = re.split(r'(?<=[.!?]) +', agent_reply)

return {
        'messages': sentences
    }