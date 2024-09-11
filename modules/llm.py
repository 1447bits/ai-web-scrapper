# splitting text in batches

def split_dom_content(dom_content, max_len=6000):
    return [
        dom_content[i : i + max_len] for i in range(0, len(dom_content), max_len)
    ]


from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


def parse_with_ollama(dom_chunks, parse_description):

    model = OllamaLLM(model='llama3.1')

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content":chunk, "parse_description":parse_description})

        parser=StrOutputParser()
        parsed_result = parser.invoke(response)
        parsed_results.append(parsed_result)

    return "\n".join(parsed_results)


# ------------------------------------------------------------

import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


def parse_with_groq(dom_chunks, parse_description):

    load_dotenv()

    groq_api_key=os.getenv("groq_api_key")
    model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):

        response = chain.invoke({"dom_content":chunk, "parse_description":parse_description})

        # print(f"parsed batch {i} of {len(dom_chunks)}")
        
        parser=StrOutputParser()
        parsed_result = parser.invoke(response)
        parsed_results.append(parsed_result)

    return "\n".join(parsed_results)
