from openai import Client
from api_key import key
import time

client = Client(api_key=key)

file = client.files.create(
    file=open("attention_is_all_you_need.pdf", "rb"),
    purpose='assistants'
)

tone = int(input("Please select the tone of the response you want : \n1. Academic\n2. Creative\n3. Aggressive\n"))
length = int(input("Please select the response length you need : \n1. Short\n2. Medium\n3. Long\n"))

tone = "Academic" if tone==1 else "Creative" if tone==2 else "Aggressive"
length = "Short" if length == 1 else "Medium" if length == 2 else "Long"

# print(tone, " and ", length)


assistant = client.beta.assistants.create(
    name="Research Assistant",
    description=f"You are a research assistant. You would respond to user's queries regarding any research paper they share. Your response should be {tone} and output length should be {length}. ",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
)

thread = client.beta.threads.create()

for i in range(3) :
    
    user_input = input("\nUser : ")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
        # file_ids=[file.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print("\nAssistant : " , messages.data[0].content[0].text.value)

client.files.delete(file.id)