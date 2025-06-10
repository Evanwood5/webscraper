import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_openai

# Title
st.title("AI Web Scraper")

# Input URL
url = st.text_input("Enter a Website URL: ")

# Scrape button
if st.button("Scrape Site"):
    st.write("Scrape Site")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content

    # View scraped DOM content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Parsing section
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_openai(dom_chunks, parse_description)

            st.markdown("### Results:")
            for message in result:
                st.markdown(f"- {message.content.strip()}")
