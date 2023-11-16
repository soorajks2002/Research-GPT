from openai import Client
from api_key import key
import time

client = Client(api_key=key)


system_prompt = '''You have to generate answers to a given problem statement based on the information you are provided with. The user would provide both the problem statement and the source from which the answer needs to be generated. The user's input will always follow the given format

Question : 

Source 1 author :
Source 1 data :

Source 2 author :
Source 2 data :

The number of sources could be different, like some cases might have 1, 2, 3 or n numbers of sources.
The answer must be generated strictly based on data provided by the user from different sources.
And most importantly, your response should always have a citation of the author wherever you are using the source written by them, and it should follow the traditional citation format i.e. (author_name, et al.).'''

sample_input_1 = '''Question: What is the difference between GPT and BERT models?

Source 1 author: Trinita Roy
Source 1 text: BERT is an encoder transformer model which is trained on two tasks - masked LM and next sentence prediction.

Source 2 author: Asheesh Kumar
Source 2 text: GPT is a decoder model that works best on sequence generation tasks.

Source 3 author: Siddhant Jain
Source 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have limitations in processing long texts.'''

sample_input_2 = '''Question: Why  is positional encoding needed ?
Source 1 author: Priya Patel
Source 1 text: Positional encoding is crucial in transformer models like GPT and BERT to provide information about the positions of words in a sequence. Without positional encoding, these models may struggle to understand the sequential order of words in a sentence.

Source 2 author: Rajesh Singh
Source 2 text: In natural language processing models, like GPT and BERT, positional encoding is essential for capturing the temporal relationships between words. It enables the model to discern the position of each token in a sequence, contributing to a more accurate understanding of the context.'''

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": sample_input_1}
    ],
    temperature=0.2,
    top_p=0.2,
    frequency_penalty=0.3,
    presence_penalty=0.2,
)

print(completion.choices[0].message.content)
