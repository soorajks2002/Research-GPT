from openai import Client
from api_key import key
import time
import sys
import json

client = Client(api_key=key)


def load_document(document_path):
    '''Creates OpenAI file object for the document at the given file path and returns it's file.id'''

    file = client.files.create(
        file=open(document_path, "rb"),
        purpose='assistants'
    )

    return file.id


def load_assistant(file_id):
    '''Creates an AI-Assistant which will act as a Research Assistant. Assistant will have retrieval capabilities with the file whose file.id is provided'''

    assistant = client.beta.assistants.create(
        name="Research Assistant",
        description=f"You are responsible for assisting users with their queries regarding research papers that they share. Your answer to user queries must be generated strictly based on data avialabel in the research paper.",
        model="gpt-3.5-turbo-1106",
        tools=[{"type": "retrieval"}],
        file_ids=[file_id],
    )

    return assistant.id


def extract_abstract(thread_id, assistant_id):
    '''Extracts the complete abstract part from the file shared with the assistant whoose assistant.id is shared'''

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="Get the abstract of the paper",
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status != "completed":

        time.sleep(1)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    return json.dumps({"response" : messages.data[0].content[0].text.value}, indent=4)


def paraphrase_abstract(thread_id, assistant_id, tone, length):
    '''Paraphrase the abstract from the research paper with given tone and length of response.'''

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Paraphrase the abstract with {tone} tone and {length} the abstract from the paper in terms of length",
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status != "completed":

        time.sleep(1)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    return json.dumps({"response":messages.data[0].content[0].text.value}, indent=4)


if __name__ == "__main__":

    research_paper_path = "attention_is_all_you_need.pdf"

    file_id = load_document(research_paper_path)

    assistant_id = load_assistant(file_id)

    thread = client.beta.threads.create()

    gpt_abstract_response = extract_abstract(thread.id, assistant_id)
    
    # PRINTING JSON RESPONSE 
    json_response = json.loads(gpt_abstract_response)
    print(f"\nAbstract ::\n{json_response['response']}\n\n")
    

    tone = int(input(
        "Please select the tone of the praphrase you want : \n1. Academic (default)\n2. Creative\n3. Aggressive\n"))
    length = int(input(
        "Please select the response length of paraphrase : \n1. Same length (default)\n2. Twice the length\n3. Thrice the length\n"))

    tone = "Aggressive" if tone == 3 else "Creative" if tone == 2 else "Academic"
    length = "thrice the length of " if length == 3 else "twice the length of " if length == 2 else "same length as"

    gpt_paraphrase_response = paraphrase_abstract(thread.id, assistant_id, tone, length)
    
    # PRINTING JSON RESPONSE 
    json_response = json.loads(gpt_paraphrase_response)
    print(f"\n\nParaphrased Abstract ::\n{json_response['response']}\n\n")

    client.files.delete(file_id)
