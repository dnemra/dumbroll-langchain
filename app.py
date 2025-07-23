import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load OpenAI API key securely
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("📊 Rent Roll Standardizer using GPT + LangChain")

uploaded_file = st.file_uploader("Upload your unstructured rent roll Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write("✅ Raw Input:")
        st.dataframe(df)

        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in cleaning and structuring messy rent roll data into standardized format. Convert it based on prior examples."),
            ("human", "Here is an example of the raw rent roll:\n{input}\nReturn a clean and structured version.")
        ])

        # Set up GPT-4 via LangChain
        llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0
)

        chain = prompt | llm

        # Invoke the chain with the uploaded Excel content as input
        prompt_input = df.to_csv(index=False)
        response = chain.invoke({"input": prompt_input})

        # Display GPT output
        st.markdown("### ✅ Standardized Output")
        st.write(response.content)

        # Optionally allow export
        st.download_button("Download as Text", response.content, file_name="standardized_output.txt")

    except Exception as e:
        st.error(f"❌ Error: {e}")
