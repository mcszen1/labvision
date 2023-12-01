def main():
    st.image('labcom_logo_preto.jpg')
    st.title("Calculadora de Calorias")
    st.write('Saiba quanto está ingerindo')
    st.write('Use uma imagem de arquivo ou tire uma foto com sua câmera')
    df = pd.read_csv('tabelacal.csv')
    tabela_calorias = df.set_index('Descrição')['Calorias (Kcal)'].to_dict()

    option = st.radio('Escolha a origem da sua imagem:', ('Arquivo', 'Camera'))
    if option == "Arquivo":
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
                # total= calcular_calorias_do_prato(description, tabela_calorias)
                # st.write("Total de Calorias: ", total)
 
                
    if option == 'Camera':
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
                
                # Display the description 
                st.write("Description: ", description)

                # Calcular calorias
                total= calcular_calorias_do_prato(description, tabela_calorias)
                st.write("Total de Calorias: ", total)

if __name__ == '__main__':
    main()
