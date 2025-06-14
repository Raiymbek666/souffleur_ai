from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config.config import DB_CONNECTION_STRING

Base = declarative_base()
engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Dialog(Base):
    __tablename__ = "dialogs"

    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="dialog")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    dialog_id = Column(Integer, ForeignKey("dialogs.id"))
    sender = Column(String)
    text = Column(String)
    time = Column(String)

    dialog = relationship("Dialog", back_populates="messages")


class KrbUserProfile(Base):
    __tablename__ = "krb_user_profiles"

    # Primary key for KRB users
    phone = Column(String, primary_key=True, index=True)

    # The selected 17 columns
    product = Column(String)
    cont_code = Column(String)
    currency = Column(String)
    od = Column(String) # Using String for simplicity in RAG
    pr_od = Column(String)
    day_pr_od = Column(String)
    stav = Column(String)
    end_date = Column(String)
    pog = Column(String)
    loan_status = Column(String)
    beg_date = Column(String)
    purpose = Column(String)
    vid_zal = Column(String)
    im_obesp_tng = Column(String)
    totaldebt = Column(String)
    rate_effective = Column(String)
    fSubsGosProg = Column(String)

    def __repr__(self):
        return f"<KrbUserProfile(phone='{self.phone}', product='{self.product}')>"

class MmbUserProfile(Base):
    __tablename__ = "mmb_user_profiles"

    # Primary key for MMB users
    call_id = Column(String, primary_key=True, index=True)

    # The same 17 columns
    product = Column(String)
    cont_code = Column(String)
    currency = Column(String)
    od = Column(String)
    pr_od = Column(String)
    day_pr_od = Column(String)
    stav = Column(String)
    end_date = Column(String)
    pog = Column(String)
    loan_status = Column(String)
    beg_date = Column(String)
    purpose = Column(String)
    vid_zal = Column(String)
    im_obesp_tng = Column(String)
    totaldebt = Column(String)
    rate_effective = Column(String)
    fSubsGosProg = Column(String)

    def __repr__(self):
        return f"<MmbUserProfile(call_id='{self.call_id}', product='{self.product}')>"