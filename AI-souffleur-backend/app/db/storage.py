from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.interface import Dialog, Message


def save_dialog_to_db(call_id: str, messages_data: list, db: Session):
    now = datetime.now()
    dialog = Dialog(call_id=call_id, created_at=now)
    db.add(dialog)
    db.commit()
    db.refresh(dialog)

    saved_messages = []

    for idx, msg in enumerate(messages_data):
        # Генерация времени, если не указано
        time_offset = (idx // 2)
        msg_time = msg.time or (now + timedelta(minutes=time_offset)).strftime("%H:%M")

        message = Message(
            dialog_id=dialog.id,
            sender=msg.from_,
            text=msg.text,
            time=msg_time
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        saved_messages.append({
        "id": str(message.id),
        "call_id": call_id,  # <-- вот это важно!
        "from_": message.sender,
        "text": message.text,
        "time": message.time
    })

    return {
        "call_id": call_id,
        "created_at": dialog.created_at.isoformat(),
        "messages": saved_messages
    }

def add_message_to_dialog(call_id: str, sender: str, text: str, db: Session):
    # найти диалог
    dialog = db.query(Dialog).filter(Dialog.call_id == call_id).first()
    if not dialog:
        raise ValueError(f"Dialog with call_id {call_id} not found")

    # посчитать время на основе текущего количества сообщений
    message_count = db.query(Message).filter(Message.dialog_id == dialog.id).count()
    time_offset = message_count // 2
    now = datetime.now()
    msg_time = (now + timedelta(minutes=time_offset)).strftime("%H:%M")

    # создать и сохранить сообщение
    message = Message(
        dialog_id=dialog.id,
        sender=sender,
        text=text,
        time=msg_time
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # получить все сообщения по этому диалогу
    all_messages = db.query(Message).filter(Message.dialog_id == dialog.id).order_by(Message.id).all()

    # вернуть список сообщений
    return [
        {
            "id": str(msg.id),
            "call_id": call_id,
            "from_": msg.sender,
            "text": msg.text,
            "time": msg.time
        }
        for msg in all_messages
    ]