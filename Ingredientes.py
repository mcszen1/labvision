import base64
import streamlit as st
import pyttsx3
import os
import tempfile
import requests, uuid, json
import azure.cognitiveservices.speech as speechsdk
from openai import OpenAI
import json

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def save_uploaded_file(uploaded_file_content):
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file_content)
    return "temp_image.jpg"

def analyze_image_with_openai(image):
    # This function will send a request to OpenAI's GPT-4 Vision API to analyze the image.
    # The 'image' parameter can be a URL or base64-encoded data.
    # Here we provide a mock-up of the API call with placeholder response handling.

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image? Answer in Portuguese"},
                    {"type": "image_url", "image_url": image},
                ],
            }
        ],
        max_tokens=300,
    )
    description_content = response.choices[0].message.content
    print(description_content)
    
    return description_content

def encontrar_ingrediente_semelhante(ingrediente, opcoes):
    ingrediente_semelhante, similaridade = process.extractOne(ingrediente, opcoes)
    if similaridade > 60:  # Definir um limiar de similaridade
        return ingrediente_semelhante
    return None

# Calcular as calorias do prato
def calcular_calorias_do_prato(ingredientes, tabela_calorias):
    total_calorias = 0
    for ingrediente in ingredientes:
        ingrediente_encontrado = encontrar_ingrediente_semelhante(ingrediente, tabela_calorias.keys())
        if ingrediente_encontrado:
            total_calorias += tabela_calorias.get(ingrediente_encontrado, 0)
        else:
            st.write(f"Ingrediente não encontrado ou muito diferente: {ingrediente}")
    return total_calorias

def main():
    st.image('labcom_logo_preto.jpg')
    st.title("Calculadora de Calorias")
    st.write('Saiba quanto está ingerindo')
    st.write('Use uma imagem de arquivo ou tire uma foto com sua câmera')
    df = pd.read_csv('tabelacal.csv')
    tabela_calorias = df.set_index('Descrição')['Calorias (Kcal)'].to_dict()

    option = st.radio('Escolha a origem da sua imagem:',('Arquivo', 'Camera'))
    if option=="Arquivo":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            temp_path1 = save_uploaded_file(uploaded_file.read())
    
            st.image(temp_path1, caption="Image fornecida", use_column_width=True)

            if uploaded_file is not None:
                # Convert the file to an image URL or base64-encoded string as required by OpenAI API
                image_data = uploaded_file.getvalue()
                image_url = "data:image/jpg;base64," + base64.b64encode(image_data).decode()
        
                # Analyze the image with OpenAI's GPT-4 Vision API
                description = analyze_image_with_openai(image_url)
                
               
                # Display the description 
                st.write("Description: ", description)

		# Calcular calorias
		total= calcular_calorias_do_prato(description, tabela_calorias)
		st.write("Total de Calorias: ", total)
 
                
    if option=='Camera':
        picture = st.camera_input("Tire uma foto")

        if picture:
            temp_path = save_uploaded_file(picture.read())
            st.image(temp_path, caption="Foto tirada", use_column_width=True)
    
   
            if picture is not None:
                # Convert the file to an image URL or base64-encoded string as required by OpenAI API
                image_data = picture.getvalue()
                image_url = "data:image/jpg;base64," + base64.b64encode(image_data).decode()
        
                # Analyze the image with OpenAI's GPT-4 Vision API
                description = analyze_image_with_openai(image_url)
                
                # Translate description to Portuguese
                #translated_description = translate_to_portuguese(description)
                
                # Display the description and translated text
                st.write("Description: ", description)
                #st.write("Translated Description: ", translated_description)
                
                # Convert the description to speech
                tts(description)

if __name__ == '__main__':
    main()

