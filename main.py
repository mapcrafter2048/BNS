import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="NyayaSahayak", layout="wide")
st.title("NyayaSahayak")
st.caption("BNS legal information assistant")

api_key = st.secrets["DATABRICKS_TOKEN"]
base_url = st.secrets["AI_GATEWAY_BASE_URL"]

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

SYSTEM_PROMPT = """You are a legal information assistant for the Bharatiya Nyaya Sanhita (BNS).

Answer the user's question in simple English.
Do not invent sections or punishments.
If the answer is not clearly known, say that the available information is insufficient.
At the end, include: "This is legal information, not legal advice."
"""

demo_queries = [
    "what punishments are available under the Bharatiya Nyaya Sanhita",
    "what is organized crime under BNS",
    "what is the punishment for attempt to murder under BNS",
    "what is causing death by negligence under BNS",
    "what is the difference between murder and culpable homicide not amounting to murder under BNS",
]

if "picked_query" not in st.session_state:
    st.session_state["picked_query"] = "punishment for murder under BNS"

query = st.text_input("Ask a BNS question", value=st.session_state["picked_query"])

with st.expander("Quick demo queries"):
    for q in demo_queries:
        if st.button(q, key=q):
            st.session_state["picked_query"] = q
            st.rerun()

if st.button("Ask"):
    with st.spinner("Generating answer..."):
        response = client.chat.completions.create(
            model="databricks-gemma-3-12b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            max_tokens=1200
        )
        answer = response.choices[0].message.content

    st.subheader("Answer")
    st.write(answer)
