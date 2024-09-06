import streamlit as st
from modules.scrape import (
    scrape_website, 
    extract_body_content, 
    clean_body_content
)

from modules.llm import split_dom_content, parse_with_ollama

st.title("AI Web Scrapper")
url = st.text_input("Enter web Url please :)")

if st.button("scrape site"):
    st.write("scrapping the website")

    res = scrape_website(url)
    body_content = extract_body_content(res)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("view DOM content"):
        st.text_area("DOM content", cleaned_content, height=600)


if "dom_content" in st.session_state:
    parse_description = st.text_area("How may i help you :)")

    if st.button("get response"):
        if(parse_description):
            st.write("parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)

            st.write(result)