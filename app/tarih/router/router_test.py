from fastapi import Depends
from app.utils import AppModel
from ..service import Service, get_service
from . import router

@router.post("/users/me")
def send_message(
    user_query: str,
    conversation_id: str,
    svc: Service = Depends(get_service),
):  
    tulga = svc.tarih.get_tulga()
    conv_id = svc.repository.create_conversation(conversation_id)
    if user_query:
        svc.repository.append_conversation(conversation_id,role="user",content=content)
        response = svc.openai.get_completion(msg=user_query)  #request to chatgpt
        response_message = response["choices"][0]["message"]
    
    if response_message.get("function_call"):
        print("HELLO")
        fn_name = response_message["function_call"]["name"]
        print(fn_name)
        print("LOH")
        if fn_name == "get_bot_response_tulga":
            print("fn_name_condition")
            bot_response = svc.openai.get_bot_response_tulga(user_query,tulga["persist"])
            print("fn_name_post_condition")
        elif fn_name == "get_bot_response_tarih":
            print("fn_name_elif")
            bot_response = svc.openai.get_bot_response_tarih(user_query,tulga["persist"])
            print("fn_name_post_elif")
        elif fn_name == "get_bot_response_personality":
            print("fn_name_elif")
            bot_response = svc.openai.get_bot_response_personality(user_query,tulga["persist"])
            print("fn_name_post_elif")
        else:
            bot_response = svc.openai.get_bot_response_tarih(user_query,tulga["persist"])

        svc.repository.append_conversation(conversation_id, role="bot", content=bot_response)

    return {
        "user":content,
        "bot":bot_response 
        }
