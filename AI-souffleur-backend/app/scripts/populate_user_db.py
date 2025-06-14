import pandas as pd
from sqlalchemy.orm import sessionmaker
from app.db.interface import Base, engine, KrbUserProfile, MmbUserProfile

SELECTED_COLUMNS = [
    'product', 'cont-code', 'currency', 'od', 'pr-od', 'day-pr-od',
    'stav', 'end-date', 'pog', 'loan-status', 'beg-date', 'purpose',
    'vid-zal', 'im-obesp-tng', 'totaldebt', 'rate_effective', 'fSubsGosProg'
]

Session = sessionmaker(bind=engine)

def populate_krb_users():
    print("Populating KRB user profiles...")
    db = Session()
    try:
        pk_column_name = 'Номер телефона'
        required_cols = [pk_column_name] + SELECTED_COLUMNS
        
        df = pd.read_csv(
            '/project/app/knowledge_base/КРБ/Данные/krb_users.csv', 
            encoding='cp1251', 
            sep=';'
        )
        
        df = df[required_cols]
        df.columns = df.columns.str.replace('-', '_')
        df.rename(columns={pk_column_name.replace('-', '_'): 'phone'}, inplace=True)
        
        records = df.to_dict(orient='records')
        
        for record in records:
            user_profile = KrbUserProfile(**record)
            db.merge(user_profile)
            
        db.commit()
        print(f"Successfully processed {len(records)} KRB user records.")
    except Exception as e:
        print(f"An error occurred during KRB population: {e}")
        db.rollback()
    finally:
        db.close()

def populate_mmb_users():
    print("Populating MMB user profiles...")
    db = Session()
    try:
        pk_column_name = 'CALL_ID' 
        required_cols = [pk_column_name] + SELECTED_COLUMNS
        
        df = pd.read_csv('/project/app/knowledge_base/ММБ/Данные/mmb_users.csv', encoding='cp1251', sep=';')
        
        df = df[required_cols]
        df.columns = df.columns.str.replace('-', '_')
        
        df.rename(columns={pk_column_name: 'call_id'}, inplace=True)
        
        records = df.to_dict(orient='records')
        
        for record in records:
            user_profile = MmbUserProfile(**record)
            db.merge(user_profile)
            
        db.commit()
        print(f"Successfully processed {len(records)} MMB user records.")
    except Exception as e:
        print(f"An error occurred during MMB population: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Setting up database tables...")
    Base.metadata.create_all(bind=engine)
    
    populate_krb_users()
    populate_mmb_users()
    
    print("Database population complete.")