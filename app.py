import streamlit as st
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq  # ✅ Groq integration for LangChain

# 🔐 Load Groq API key from secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# 🎯 UI
st.title("📊 Rent Roll Standardizer (Groq + LangChain)")

uploaded_file = st.file_uploader("Upload your messy rent roll (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # ✅ Load Excel data
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write("✅ Raw Input")
        st.dataframe(df)

        # 📉 Limit large files
        prompt_input = df.head(100).to_csv(index=False)[:15000]

        # 💬 Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a real estate analyst. Your job is to standardize rent roll data into clean tabular format. Return only the cleaned table."),
            ("human", "Here is the raw rent roll:\n{input}")
        ])

        # 🤖 Connect to Groq
        llm = ChatGroq(
            api_key=groq_api_key,
            model_name="mixtral-8x7b-32768",  # ✅ free + very fast
            temperature=0
        )

        chain = prompt | llm
        response = chain.invoke({"input": prompt_input})

        # 📋 Display result
        st.markdown("### ✅ Standardized Output")
        st.write(response.content)

        st.download_button("📥 Download Output", response.content, file_name="cleaned_rentroll.txt")

    except Exception as e:
        st.error(f"❌ Error: {e}")
