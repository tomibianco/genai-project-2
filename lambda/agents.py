


def function():    
    # Cargar el prompt JSON
    prompt = prompt_s3()

    # Configurar modelo LangChain
    chat = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Crear mensaje con los datos del JSON
    messages = [
        SystemMessage(content=prompt["role"] + " " + prompt["instructions"] + " " + prompt["context"]),
        HumanMessage(content="Explica el proceso de extracción de litio")
    ]











sentences = re.split(r'(?<=[.!?]) +', agent_reply)

return {
        'messages': sentences
    }