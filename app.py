import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(
    page_title="AI Chain"
)

st.sidebar.header("Groq Chat")
st.header("AI Language Chain")

api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get free API key at console.groq.com")

model_name = st.sidebar.selectbox(
    "Model",
    ["llama-3.1-8b-instant", "groq/compound-mini"],
    index=0
    )

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []



if "messages" not in st.session_state:
    st.session_state.messages = []

# initialize llm
def get_chain(api_key, model_name):
    if not api_key:
        return None
    llm = ChatGroq(groq_api_key=api_key,
             model_name= model_name,
             temperature=0.7,
             streaming=True
            )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant powered by Groq. Answer questions clearly and concisely"),
        ("user", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain
    
chain = get_chain(api_key, model_name)

if not chain:
    st.warning("Please enter your Groq API key in the sidebar to start chatting!")
else:

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if question:= st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_resp = ""

            try:
                for chunk in chain.stream({"question": question}):
                    full_resp += chunk
                    message_placeholder.markdown(full_resp+ "")
                message_placeholder.markdown(full_resp)

                st.session_state.messages.append({"role": "assistant", "content": full_resp})
            except Exception as e:
                st.error(f"Error: {str(e)}")