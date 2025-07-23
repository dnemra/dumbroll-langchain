import streamlit as st
import pandas as pd
from langchain_community.chat_models import ChatTogether
from langchain.prompts import ChatPromptTemplate

# ✅ Load Together API key from Streamlit secrets
together_api_key = st.secrets["TOGETHER_API_KEY"]

# ✅ Streamlit UI
st.title("📊 Rent Roll Standardizer (Together.ai + LangChain)")

uploaded_file = st.file_uploader("Upload your unstructured rent roll Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # ✅ Read Excel input
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write("✅ Raw Input:")
        st.dataframe(df)

        # ✅ Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in cleaning and structuring messy rent roll data into a clean table. Focus on standardizing property/unit/rent/deposit info."),
            ("human", """Here is the raw rent roll data:
{input}
Return a clean, standardized table with consistent column headers.""")
        ])

        # ✅ Set up Together.ai LLM
        llm = ChatTogether(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # You can change to other Together models
            temperature=0,
            together_api_key=together_api_key
        )

        # ✅ Combine LangChain prompt and model
        chain = prompt | llm

        # ✅ Format DataFrame into a string for the prompt
        prompt_input = df.to_csv(index=False)

        # ✅ Run the model
        response = chain.invoke({"input": prompt_input})

        # ✅ Display result
        st.markdown("### ✅ Standardized Output")
        st.write(response.content)

        # ✅ Allow download
        st.download_button("📥 Download as Text", response.content, file_name="standardized_output.txt")

    except Exception as e:
        st.error(f"❌ Error: {e}")
