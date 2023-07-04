
from datetime import datetime

import json
import os
import requests
from dotenv import load_dotenv, find_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
import textwrap
import langchain

langchain.debug = True


def ask_HuggingFace_model(user_info, repo_id="tiiuae/falcon-7b-instruct"):

    falcon_llm = HuggingFaceHub(
        repo_id=repo_id,
        model_kwargs={"temperature": 0.01, "max_new_tokens": 100}
    )

    template = """Imagine you work in an immigration department and you need
    to summarize the following personal information with as many details as
    possible. This information is extracted from the person's identity card.
    As far as gender is concerned, check the field \"sexe\". M means man and
    F means woman. Today is {date}. Don't make any assumption about the person,
    and try to answer the following question:

    Question:
    {question}

    User information:
    {user_info}
    """

    now = datetime.now()
    prompt = PromptTemplate(
        template=template, input_variables=["question", "user_info", "date"])
    llm_chain = LLMChain(prompt=prompt, llm=falcon_llm)

    question = "Can you summarize the known information about this person?"
    response = llm_chain.run(
        {"question": question, "user_info": user_info,
         "date": now.strftime("%d/%m/%Y")})
    wrapped_text = textwrap.fill(
        response, width=100, break_long_words=False, replace_whitespace=False
    )
    print(wrapped_text)


def docteller_parsing(file_path):

    with open(file_path, "rb") as f:
        image_bytestream = f.read()

    def parse_document_with_docteller(image_bytestream):
        request_payload = {
            "payload": image_bytestream,
        }
        return requests.post(
            "https://api.docteller.com/v1/read",
            headers={"access_token": DOCTELLER_API_KEY},
            files=request_payload,
        )

    response = parse_document_with_docteller(image_bytestream)

    try:
        return response.json()
    except json.JSONDecodeError:
        print(response.status_code, response.text)
        exit(-1)


if __name__ == "__main__":

    load_dotenv(find_dotenv())
    HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
    DOCTELLER_API_KEY = os.environ["DOCTELLER_API_KEY"]

    file_path = "ID_test.jpg"

    user_info = docteller_parsing(file_path)

    info = ("{"+str(user_info['documents'][0]["fields"])
            .replace("_", " ").replace("\'", "").replace("{", " ")
            .replace("}", " ").replace(", ", "\n ")+"}")

    ouput = ask_HuggingFace_model(info)

    print(ouput)
