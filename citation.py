from openai import Client
from api_key import key
import time

client = Client(api_key=key)


system_prompt = '''You would be given a problem statement and few sources regarding the problem statement that includes the context and the authors name.
Source format is as follows :
Source 1 author : author name
Source 1 text : textual data
You have to generate an answer for the problem statement based on the sources provided. And in addition to the response generated you would have to add proper citation regarding the source in your respoonse.'''

sample_input = '''Question: What is the difference between GPT and BERT models?

Source 1 author: Trinita Roy
Source 1 text: BERT is an encoder transformer model which is trained on two tasks - masked LM and next sentence prediction.

Source 2 author: Asheesh Kumar
Source 2 text: GPT is a decoder model that works best on sequence generation tasks.

Source 3 author: Siddhant Jain
Source 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have limitations in processing long texts.'''

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": sample_input}
    ]
)

print(completion.choices[0].message.content)
