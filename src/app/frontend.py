# Frontend page

import streamlit as st
import requests



# Set name of the page with its icon
st.set_page_config(
    page_title = "ScholarAI", 
    page_icon = "📚"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style="text-align: center;">
    📚 ScholarAI
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="text-align: center;">
    AI-Powered Research Paper Assistant
    </h3>
    """,
    unsafe_allow_html=True
)



st.divider()


st.markdown(
        "<p style='text-align: center;'>Ask questions about your research papers and get answers with sources.</p>",
        unsafe_allow_html=True
)

st.space()
st.space()

col1, col2, col3 = st.columns([1, 20, 1])

with col2:  

    with st.form("question_form"):
        # User input
        question = st.text_input("Ask a question:", placeholder="Example: Explain the attention mechanism in Transformers")


        button_col1, button_col2, button_col3 = st.columns([2, 1, 2])

        with button_col2:
            submit = st.form_submit_button("🔍 Search") # The code inside runs only when the user clicks it and the API call happnes 


# run only after clicking the button
if submit:

    # Check if the user entered a question (if question has a value)
    if question:


            with st.spinner("Searching papers and generating answer...", width="stretch"):


                # Streamlit app sends an HTTP POST request.
                response = requests.post(
                    "http://localhost:8000/ask", # Send to this address
                    json = { # This information
                        "question": question
                    }
                )

            # If we get the answer
            if response.status_code == 200:

                data = response.json() # convert to json the answer

                st.subheader("Answer")

                st.write(data["answer"])

                st.subheader("Sources")

                for source in data["sources"]:
                    st.write(
                        f"- 📄 {source}"
                    )

            else:
                st.error(f"Status Code: {response.status_code}")
                st.write(response.text)


