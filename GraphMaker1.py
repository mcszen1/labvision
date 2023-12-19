import streamlit as st
import pandas as pd
import os
from openai import OpenAI

client = OpenAI()
os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
resposta=""


def generate_response(input_text):

  response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {
      "role": "system",
      "content":"You are a network graph maker who extracts terms and their relations from a given text. Scan all the provided text, from the begining to the end, and try to collect the bigger possible number of nodes and edges. DO NOT extract only samples but all the nodes and edges you can find. Translate all you outputs , including labels at the graph in brazilian portuguese . Consider PROCEDURES and GRAPH PREFERENCES.PROCEDURES= 1 - You are provided with a context chunk (delimited by ```) Your task is to extract the ontology  of terms mentioned in the given context. These terms should represent the key concepts as per the context. 2: While traversing through each sentence, Think about the key terms mentioned in it.Terms may include object, entity, location, organization, person, condition, acronym, documents, service, concept, etc.Terms should be as atomistic as possible.3: Think about how these terms can have one on one relation with other terms.Terms that are mentioned in the same sentence or the same paragraph are typically related to each other.Terms can be related to many other terms.4: Find out the relation between each such related pair of terms.Format your output as a CSV file. Each element of the list contains a pair of terms and the relation between them, like the follwing collumns order:Node 1, Edge, Node 2. GRAPH PREFERENCES = When creating the graph, please follow these specific instructions to ensure clarity and legibility:Visibility of Labels: Ensure that all labels of nodes and edges are clearly visible. Avoid any text overlaps and make sure each label can be easily read. Use a Fruchterman Reingold distribuition with scale = 1000 e k=1Font Size: Increase the font size for the labels of the nodes and the lables of the edges, to facilitate reading. The labels should be large enough to be read effortlessly in a standard size view.Gravity Parameter: Set the gravity parameter (in the graph layout) to the lowest possible value. The goal is to maximize the distance between nodes and prevent any overlap, ensuring a clear distinction between each node and its connections."},
    {
      "role": "user",
      "content": input_text
    }
  ],
  temperature=0.7,
  max_tokens=2048
)
  
  assistant_message = response.choices[0].message.content.strip()
  return assistant_message


st.image("labcom_logo_preto.jpg",use_column_width="False")
# Título do Aplicativo
st.title('GRAPH MAKER')
input_text=st.text_input('Entre com o texto para análise')
if input_text:
  with st.spinner("📟 Analisando seu texto. Aguarde."):
            resposta=generate_response(input_text)
            st.write(resposta)
