# fastapi 

# принимать с фронта дсончики, и вызывать функции из этого же репозитория

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.interface import SessionLocal, Base, engine, Dialog, Message
from app.api.models import IncomingDialog, FullResponse, DialogResponse, MessageOut, ClientInfo, Suggestion, IncomingMessage
from app.db.storage import save_dialog_to_db, add_message_to_dialog
from app.rag.rag_builder import create_rag_chain
from app.utils.rag_formatter import convert_messages_to_rag_format

rag_chain = create_rag_chain()

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно временно ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/dialogs", response_model=FullResponse)
def save_dialog(dialog: IncomingDialog, db: Session = Depends(get_db)):
    result = save_dialog_to_db(dialog.call_id, dialog.messages, db)

    try:
        rag_input = convert_messages_to_rag_format(result["messages"], call_id=dialog.call_id)
        suggestions = rag_chain.run_request(rag_input, db, k=3)
    except Exception as e:
        suggestions = [{
            "text": "RAG недоступен",
            "type": "answer",
            "source": "none",
            "confidence": 0
        }]

    return FullResponse(
        status="ok",
        dialog=DialogResponse(
            call_id=result["call_id"],
            created_at=result["created_at"],
            client=ClientInfo(),
            messages=[MessageOut(**msg) for msg in result["messages"]]
        ),
        suggestions=suggestions
    )

@app.post("/api/message") #add_message
def add_message(msg: IncomingMessage, db: Session = Depends(get_db)):
    try:
        saved_msg = add_message_to_dialog(msg.call_id, msg.from_, msg.text, db)
    except ValueError as e:
        return {"status": "error", "message": str(e)}

    try:
        rag_input = convert_messages_to_rag_format(saved_msg, call_id=msg.call_id)
        suggestions = rag_chain.run_request(rag_input, db, k=3)
    except Exception as e:
        print (e)
        suggestions = [{
            "text": e,
            "type": "answer",
            "source": "none",
            "confidence": 0
        }]

    return {
        "status": "ok",
        "call_id": msg.call_id,
        "client": {
            "phone": "string",
            "name": "string",
            "contract": "string",
            "product": "string",
            "loyalty": "string"
        },
        "messages": [saved_msg],
        "suggestions": suggestions
    }

@app.get("/api/dialogs")
def get_all_messages_grouped(db: Session = Depends(get_db)):
    dialogs = db.query(Dialog).all()
    result = []

    for dialog in dialogs:
        messages = db.query(Message).filter(Message.dialog_id == dialog.id).order_by(Message.id).all()
        message_list = [
            {
                "id": str(m.id),
                "call_id": dialog.call_id,
                "from": m.sender,
                "text": m.text,
                "time": m.time
            }
            for m in messages
        ]
        result.append({
            "call_id": dialog.call_id,
            "messages": message_list
        })

    return result


@app.get("/api/messages/{call_id}")
def get_dialog_by_call_id(call_id: str, db: Session = Depends(get_db)):
    dialog = db.query(Dialog).filter(Dialog.call_id == call_id).first()

    if not dialog:
        raise Exception("The dialog not found in the system")

    messages = db.query(Message).filter(Message.dialog_id == dialog.id).order_by(Message.id).all()

    message_list = [
        {
            "id": str(m.id),
            "call_id": call_id,
            "from": m.sender,
            "text": m.text,
            "time": m.time
        }
        for m in messages
    ]

    return {
        "call_id": call_id,
        "messages": message_list
    }