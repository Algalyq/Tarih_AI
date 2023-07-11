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

class Tarih:
    def __init__(self,tulga: str = "Чокан Валиханов"):
        shoqan = "Чокан Валиханов"
        tole_bi = "Толе Би, вы не хан, вы би"
        kazybek_bi = "Казыбек Би, вы не хан, вы би"
        aiteke_bi = "Айтеке Би, вы не хан, вы би"
        abylay_khan = "Абылай Хан, Хан Казахского Ханство"
        kasym_khan = "Касым Хан, Хан Казахского Ханство"
        zhangir_khan = "Жангир Хан, Хан Казахского Ханство"
        haqnazar_khan = "Хак-Назар Хан, Хан Казахского Ханство"
        esim_khan = "Есим Хан, Хан Казахского Ханство"

        self.persist_directory_personality = "db_personality/shoqan"
        

        self.tulga = tulga
    

    def get_tulga(self):
        return {
            "tulga":self.tulga,
            "persist":self.persist_directory_personality
        }





    def change_tulga(self,input: dict):
        self.tulga = input["name"]
        if self.tulga == "Қасым Хан":
            personality = kasym_khan
            persist_directory_personality = "db_personality/kasym_khan"
        elif self.tulga == "Хақназар Хан":
            personality = haqnazar_khan
            persist_directory_personality = "db_personality/haqnazar_khan"
        elif self.tulga == "Есім Хан":
            personality = esim_khan
            persist_directory_personality = "db_personality/esim_khan"
        elif self.tulga == "Салқам Жәнгір Хан":
            personality = zhangir_khan
            persist_directory_personality = "db_personality/zhangir_khan"
        elif self.tulga == "Абылай Хан":
            personality = abylay_khan
            persist_directory_personality = "db_personality/abylay_khan"
        elif self.tulga == "Төле Би":
            personality = tole_bi
            persist_directory_personality = "db_personality/tole_bi"
        elif self.tulga == "Қазыбек Би":
            personality = kazybek_bi
            persist_directory_personality = "db_personality/kazybek_bi"
        elif self.tulga == "Әйтеке Би":
            personality = aiteke_bi
            persist_directory_personality = "db_personality/aiteke_bi"
        elif self.tulga == "Шоқан Уәлиханов":
            personality = shoqan
            persist_directory_personality = "db_personality/shoqan"

        persist_directory_tarih = "db_site"
        persist_directory_tulga = "db_tulga"


 



        # Create a function to send messages


        # Create a list to store messages

