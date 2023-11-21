from openai import Client
from api_key import key
import time

client = Client(api_key=key)


# prompt which describes the functioning of the gpt-model

system_prompt = '''You have to generate answers to a given problem statement based on the information you are provided with citation to authors of the source. The user would provide both the problem statement and the source from which the answer needs to be generated. The user's input will always follow the given format

Question : 

Source 1 author :
Source 1 text :

Source 2 author :
Source 2 text :

The number of sources could be different, like some cases might have 1, 2, 3 or n numbers of sources.
The answer you generate should only contain contents from the source text and don't add additional context to your answer.
And most importantly, your response should always have the citation of the author wherever you are using the source written by them, and it should follow the traditional citation format i.e. (author_name, et al.).
Add the citation properly don't mix up the author with different author's source.
And if you can't find nothing to create an answer from the source then return "Nothing relevant in the source text"
'''




# Sample input given in the assignment

sample_input_1 = '''Question: What is the difference between GPT and BERT models?

Source 1 author: Trinita Roy
Source 1 text: BERT is an encoder transformer model which is trained on two tasks - masked LM and next sentence prediction.

Source 2 author: Asheesh Kumar
Source 2 text: GPT is a decoder model that works best on sequence generation tasks.

Source 3 author: Siddhant Jain
Source 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have limitations in processing long texts.
'''




# Sample input to test

sample_input_2 = '''Question: Why  is positional encoding needed ?
Source 1 author: Priya Patel
Source 1 text: Positional encoding is crucial in transformer models like GPT and BERT to provide information about the positions of words in a sequence. Without positional encoding, these models may struggle to understand the sequential order of words in a sentence.

Source 2 author: Rajesh Singh
Source 2 text: In natural language processing models, like GPT and BERT, positional encoding is essential for capturing the temporal relationships between words. It enables the model to discern the position of each token in a sequence, contributing to a more accurate understanding of the context.
'''


# format of sample if you want to test the model

sample_input_3 = '''Question :

Source 1 author:
Source 1 text: 
'''

# Sample input given in the assignment

sample_input_4 = '''Question: What is LSTM ?

Source 1 author: Trinita Roy
Source 1 text: BERT is an encoder transformer model which is trained on two tasks - masked LM and next sentence prediction.

Source 2 author: Asheesh Kumar
Source 2 text: GPT is a decoder model that works best on sequence generation tasks.

Source 3 author: Siddhant Jain
Source 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have limitations in processing long texts.
'''

# Making the Opena-AI API call

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": sample_input_4}         # Replace content with the input you want to test
    ],
    temperature=0.2,                                        # Hyperparameters tuned accordingly
    top_p=0.2,
    frequency_penalty=0.3,
    presence_penalty=0.2,
)

print(f"\n{completion.choices[0].message.content}\n")
