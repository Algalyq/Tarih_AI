from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult

import os
import time
import openai
import pymongo
import streamlit as st
from datetime import datetime
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain import PromptTemplate
from dotenv import load_dotenv
from bson.objectid import ObjectId

# openai_key = os.environ["OPENAI_API_KEY"]
# openai.apall_messagesi_key = openai_key
embedding = OpenAIEmbeddings()
template = """
I can answer questions about different periods, including the Stone Age, as well as events, individuals, battles, and governments that were significant in Central Asia. 
I will answer to exact to qusetion.
Question: {question}
"""

functions = [
    {
        "name": "get_bot_response_tarih",
        "description": "Call this function if the user's query is not about persons to search the database for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_query": {
                    "type": "string",
                    "description": "User's input regarding a person or personality.",
                },
            },
            "required": ["user_query"],
        },
    },
    {
        "name": "get_bot_response_tulga",
        "description": "Call this function if the user's query is about persons to search the database for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_query": {
                    "type": "string",
                    "description": "User's query about Kazakh history or any specific individuals.",
                },
            },
            "required": ["user_query"],
        },
    },
    {
        "name": "get_bot_response_personality",
        "description": "Call this function if the user's request concerns the {personality} itself, such as asking 'who are you' to search the database for an appropriate response.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_query": {
                    "type": "string",
                    "description": "User's query about the {personality} or seeking information about its capabilities or identity.",
                },
            },
            "required": ["user_query"],
        },
    },
]

class OpenAI:
    def __init__(self,openai_key,):
        self.openai_key = openai_key
        self.chat = ChatOpenAI(
            temperature=0.4, openai_api_key=self.openai_key, model_name="gpt-3.5-turbo-0613"
        )

        self.prompt = PromptTemplate(
            input_variables=["question"],
            template=template,
        )
    
    def get_completion(self,msg):
        messages = [
            {"role": "user", "content": msg},
        ]
        response = openai.ChatCompletion.create(                model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions[-1],
            temperature=0.0,
            function_call="auto",
        )
        return response

    def get_bot_response_personality(self,user_query,persist):
        persist_directory_personality = persist
        final_prompt = self.prompt.format(question=user_query)
        main_content = final_prompt + "\n\n"
        vectordb = Chroma(
            persist_directory=persist_directory_personality,
            embedding_function=embedding,
        )
        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents(personality + ", " + user_query)
        for doc in docs:
            main_content += doc.page_content + "\n\n"
        print(main_content)
        messages.append(HumanMessage(content=main_content))
        ai_response = self.chat(messages).content
        messages.pop()
        messages.append(HumanMessage(content=user_query))
        messages.append(AIMessage(content=ai_response))

        return ai_response

    def get_bot_response_tulga(self,user_query,persist):
        persist_directory_personality = persist
        final_prompt = self.prompt.format(question=user_query)
        main_content = final_prompt + "\n\n"
        vectordb = Chroma(
            persist_directory=persist_directory_tulga, embedding_function=embedding
        )
        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents("Кто " + user_query)
        for doc in docs:
            main_content += doc.page_content + "\n\n"
       
        messages.append(HumanMessage(content=main_content))
        ai_response = self.chat(messages).content
        messages.pop()
        messages.append(HumanMessage(content=user_query))
        messages.append(AIMessage(content=ai_response))
        return ai_response

    def get_bot_response_tarih(self,user_query,persist):
        persist_directory_personality = persist
        final_prompt = self.prompt.format(question=user_query)
        main_content = final_prompt + "\n\n"
        vectordb = Chroma(
            persist_directory=persist_directory_tarih, embedding_function=embedding
        )
        retriever_tarih = vectordb.as_retriever()
        docs_tarih = retriever_tarih.get_relevant_documents("История" + user_query)
        for doc in docs_tarih:
            main_content += doc.page_content + "\n\n"
        print(main_content)
        messages.append(HumanMessage(content=main_content))
        ai_response = self.chat(messages).content

        messages.pop()
        messages.append(HumanMessage(content=user_query))
        messages.append(AIMessage(content=ai_response))

        return ai_response  