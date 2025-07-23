import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
import os
import pandas as pd

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Rent Roll Standardizer with LangChain")

uploaded_file = st.file_uploader("Upload unstructured rent roll (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📊 Original Data", df.head())

    template = ChatPromptTemplate.from_template(
        "You are a rent roll analyst. Clean and standardize this rent roll data: {input}"
    )

    import streamlit as st
from langchain.chat_models import ChatOpenAI

openai_api_key = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-4",
    temperature=0,
)

chain = template | llm


    prompt_input = df.head(10).to_csv(index=False)
    response = chain.invoke({"input": prompt_input})

    st.subheader("🧠 GPT Response")
    st.write(response.content)
