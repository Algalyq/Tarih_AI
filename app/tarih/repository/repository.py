from datetime import datetime
from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
import uuid

class History:
    def __init__(self,database: Database):
        self.database = database

    def create_conversation(self,conversation_id: str):
         # Generate a random UUID as the conversation ID
        payload = {
            "conversation_id": conversation_id,
            "history": []
        }

        self.database["conversation_db"].insert_one(payload)

        return conversation_id
    

    def append_conversation(self,conversation_id,role,content):
        self.database["conversation_db"].update_one(
                    filter={"conversation_id": ObjectId(conversation_id)},
                    update={
                        "$set": {"history":{
                                "role": role,
                                "time": datetime.now().strftime("%H:%M"),
                                "content": content,
                                            }
                                },
                    },
                )
