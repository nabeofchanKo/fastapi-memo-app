from sqlalchemy.orm import Session
from app.models import Memo
from app.schemas import MemoCreate

def create_memo(db: Session, memo:MemoCreate)->Memo:
    new_memo = Memo(title=memo.title, content=memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    
    return new_memo

def get_memos(db: Session) -> list[Memo]:
    return db.query(Memo).all()

def get_memo(db:Session, memo_id:int) -> Memo | None:
    return db.query(Memo).filter(Memo.id==memo_id).first()

def update_memo(db:Session, memo_id: int, memo: MemoCreate) -> Memo | None:
    db_memo = db.query(Memo).filter(Memo.id==memo_id).first()

    if db_memo is None:
        return None
    
    db_memo.title = memo.title
    db_memo.content = memo.content

    db.commit()
    db.refresh(db_memo)
    
    return db_memo

def delete_memo(db:Session, memo_id:int) -> Memo | None:
    db_memo = db.query(Memo).filter(Memo.id==memo_id).first()
    
    if db_memo is None:
        return
    
    db.delete(db_memo)
    db.commit()

    return db_memo