def determine_user_type(call_id: str) -> str:
    if len(call_id) == 11 and call_id.startswith("7"):
        return "KRB"
    return "MMB"


def convert_messages_to_rag_format(messages_from_db, call_id: str):
    type_ = determine_user_type(call_id)

    formatted = [
        {   
            "type": type_,
            "from": msg["from_"],
            "text": msg["text"],
            "call_id": call_id
        }
        for msg in messages_from_db
    ]
    return formatted