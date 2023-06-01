import streamlit as st
import clipboard
from langchain import PromptTemplate
from langchain.llms import OpenAI
import webbrowser
# from webbrowser import webbrowser.open()

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Email", page_icon=":robot:")

st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="## OPEN API KEY",placeholder="Example: sk-gR6RiogYUG....", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 500:
    st.write("Please enter a shorter email. The maximum length is 500 words.")
    st.stop()

generate_button_clicked = st.button("*Submit*", type='secondary', help="Click to see an example of the email you will be converting.")

st.markdown("### Your Converted Email:")

if generate_button_clicked and email_input:
    llm = load_LLM(openai_api_key="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")

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)

    st.button("Copy Email", on_click=clipboard.copy, args=(formatted_email,))
    st.markdown("#### Email copied to clipboard!")

    # st.markdown("### Compose Email")
    # gmail_link = "https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=&body=" + formatted_email.replace("\n", "%0A")

    # st.markdown(f"[Open Gmail Compose]({gmail_link})")

    subject = " "
    recipient = " "
    body = formatted_email
    def open_email_compose_box(subject, body, recipient):
        mailto_link = f"mailto:{recipient}?subject={subject}&body={body}"
        webbrowser.open(mailto_link)

# Example usage
# ubject = "Hello"
# body = "This is the body of the email"
# recipient = "example@example.com"

open_email_compose_box(subject, body, recipient)
