from sqlalchemy.orm import Session

from app.db.interface import KrbUserProfile, MmbUserProfile

COLUMN_NAME_MAP = {
    'product': 'Продукт',
    'cont_code': 'Номер договора', 
    'currency': 'Валюта кредита',
    'od': 'Остаток основного долга',
    'pr_od': 'Просроченный основной долг',
    'day_pr_od': 'Дней просрочки по основному долгу',
    'stav': 'Текущая процентная ставка',
    'end_date': 'Дата полного погашения кредита',
    'pog': 'Статус погашения кредита',
    'loan_status': 'Общий статус договора',
    'beg_date': 'Дата выдачи кредита',
    'purpose': 'Цель кредитования',
    'vid_zal': 'Вид залога',
    'im_obesp_tng': 'Стоимость залогового имущества (в тенге)',
    'totaldebt': 'Общая задолженность клиента (по всем кредитам)',
    'rate_effective': 'Годовая эффективная ставка вознаграждения (ГЭСВ)',
    'fSubsGosProg': 'Государственная программа субсидирования',
}

def _format_profile_to_text(db_profile_object) -> str:

    if not db_profile_object:
        return "Данные по клиенту не найдены."

    context_lines = []
    for col_name, human_name in COLUMN_NAME_MAP.items():

        value = getattr(db_profile_object, col_name, None)
        
        if value is not None and str(value).strip() != '':
            context_lines.append(f"- {human_name}: {value}")
            
    if not context_lines:
        return "По клиенту нет доступных данных для отображения."
        
    return "Информация по клиенту:\n" + "\n".join(context_lines)

def get_formatted_user_context(db: Session, user_type: str, user_id: str) -> str:

    user_profile = None

    if user_type == "KRB":
        user_profile = db.query(KrbUserProfile).filter(KrbUserProfile.phone == user_id).first()
    elif user_type == "MMB":
        user_profile = db.query(MmbUserProfile).filter(MmbUserProfile.call_id == user_id).first()
    else:
        return "Неизвестный тип пользователя."

    return _format_profile_to_text(user_profile)