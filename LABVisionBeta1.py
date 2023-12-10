import base64
import streamlit as st
import pyttsx3
import os
import tempfile
import requests, uuid, json
from openai import OpenAI
import json

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def translate_to_portuguese(text):
    # Pegue suas chaves e endpoint das variáveis de ambiente
    key = os.environ["TRANSLATOR_KEY"]
    endpoint = os.environ["TRANSLATOR_ENDPOINT"]
    location ="eastus2"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'pt-BR'  # Set to Portuguese
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    #st.write(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

    # Verifique se a resposta tem a estrutura esperada
    if response and 'translations' in response[0] and response[0]['translations']:
        translated_text = response[0]['translations'][0]['text']
        return translated_text
    else:
        print("Unexpected response format:", response)
        return None  # ou você pode retornar o texto original se preferir

def save_uploaded_file(uploaded_file_content):
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file_content)
    return "temp_image.jpg"

def fala(text):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    # Instead of using the default speaker, we'll save the audio to a file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = 'pt-BR-AntonioNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        st.write("Síntese de Voz : ")
        st.audio(temp_file.name, format='audio/wav')
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        st.write("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                st.write("Error details: {}".format(cancellation_details.error_details))
                st.write("Did you set the speech resource key and region values?")

    # Clean up the temporary file
    os.remove(temp_file.name)

def tts(text):

    response = client.audio.speech.create(model="tts-1", voice="onyx", input=text,)
    
    response.stream_to_file("output.mp3")
    
    st.write("Síntese de Voz : ")
    st.audio('output.mp3')

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
    
    #description=json.loads(response["choices"][0])
    #print(description)
   
    # In a real scenario, handle the response and extract the description.
    # This is a placeholder for the actual API call.
    #description = response["choices"][0]["message"]["content"]
    
    return description_content

def main():
    st.image('labcom_logo_preto.jpg')
    st.title("LABCOM VISION")
    st.write('ASSISTENTE DE IDENTIFICAÇÃO E DESCRIÇÃO DE IMAGENS')
    st.write('Use uma imagem de arquivo ou tire uma foto com sua câmera')
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
                
                # Translate description to Portuguese
                #translated_description = translate_to_portuguese(description)
                
                # Display the description and translated text
                st.write("Description: ", description)
                #st.write("Translated Description: ", translated_description)
                
                # Convert the description to speech
                tts(description)
                
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
