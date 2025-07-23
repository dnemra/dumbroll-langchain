import streamlit as st
import pandas as pd
from langchain_community.chat_models import ChatTogether
from langchain.prompts import ChatPromptTemplate

# Load Together AI API key securely
together_api_key = st.secrets["TOGETHER_API_KEY"]

# Streamlit UI
st.title("📊 Rent Roll Standardizer using Together AI + LangChain")

uploaded_file = st.file_uploader("Upload your unstructured rent roll Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.write("✅ Raw Input:")
        st.dataframe(df)

        # Prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in cleaning and structuring messy rent roll data into standardized format. Convert it based on prior examples."),
            ("human", """Here is an example of the raw rent roll:
{input}
Return a clean and structured version.""")
        ])

        # Initialize Together AI model
        llm = ChatTogether(
            together_api_key=together_api_key,
            model="togethercomputer/llama-2-70b-chat",  # You can swap model here
            temperature=0
        )

        chain = prompt | llm

        # Convert DataFrame to string input for GPT
        prompt_input = df.to_csv(index=False)
        response = chain.invoke({"input": prompt_input})

        # Output results
        st.markdown("### ✅ Standardized Output")
        st.write(response.content)

        st.download_button("Download as Text", response.content, file_name="standardized_output.txt")

    except Exception as e:
        st.error(f"❌ Error: {e}")
