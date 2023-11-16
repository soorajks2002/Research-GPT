from openai import Client
from api_key import key
import time

client = Client(api_key=key)

file = client.files.create(
    file=open("attention_is_all_you_need.pdf", "rb"),
    purpose='assistants'
)

tone = "creative"
size = "small"

assistant = client.beta.assistants.create(
    name="Research Assistant",
    description=f"You are great at answering questions from given pdf document. Your answers are solely based on the research document. Your answers is always {tone} in nature and {size} in size",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="who are the authors of this research paper ?",
    file_ids=[file.id]
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

print(messages.data[0].content[0].text.value)

client.files.delete(file.id)