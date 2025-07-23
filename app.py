import streamlit as st
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

# 🔐 Load Together API key securely from secrets
together_api_key = st.secrets["TOGETHER_API_KEY"]

# 🎯 Streamlit UI
st.title("📊 Rent Roll Standardizer (Together.ai + LangChain)")

uploaded_file = st.file_uploader("Upload your unstructured rent roll Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # ✅ Read Excel input
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write("✅ Raw Input:")
        st.dataframe(df)

        # 🧠 Prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in real estate data. Clean and standardize this messy rent roll into a clean table with consistent headers like Unit, SqFt, Rent, Start Date, End Date, Fees, Deposits."),
            ("human", "Here is the raw rent roll:\n{input}\nReturn only a clean, formatted table.")
        ])

        # 🤖 Set up Together.ai LLM (using free-tier model)
        llm = ChatTogether(
            together_api_key=together_api_key,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # ✅ Free public model
            temperature=0
        )

        # 🔗 Create chain
        chain = prompt | llm

        # 📤 Feed the prompt
        prompt_input = df.to_csv(index=False)
        response = chain.invoke({"input": prompt_input})

        # 📋 Display result
        st.markdown("### ✅ Standardized Output")
        st.write(response.content)

        # 💾 Download result
        st.download_button("📥 Download as Text", response.content, file_name="standardized_rentroll.txt")

    except Exception as e:
        st.error(f"❌ Error: {e}")
