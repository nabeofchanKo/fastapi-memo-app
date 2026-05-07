from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import MemoCreate, MemoResponse
from app.database import engine, SessionLocal
from app.models import Memo
from app import crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialzie
app = FastAPI()
@app.on_event("startup")
def startup():
    Memo.metadata.create_all(bind=engine)

@app.post("/memos")
def create_memo(memo: MemoCreate, db: Session=Depends(get_db)) -> MemoResponse:
    response = crud.create_memo(db, memo)
    return response

@app.get("/memos")
def get_memos(db:Session=Depends(get_db)) -> list[MemoResponse]:
    return crud.get_memos(db)

@app.get("/memos/{memo_id}")
def get_memo(memo_id: int, db:Session=Depends(get_db)) -> MemoResponse:
    single_memo = crud.get_memo(db, memo_id)

    if single_memo is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    return single_memo

@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoCreate, db: Session = Depends(get_db)) -> MemoResponse:
    single_memo = crud.update_memo(db, memo_id, memo)

    if single_memo is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    return single_memo

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db:Session=Depends(get_db)):
    single_memo = crud.delete_memo(db, memo_id)
    
    if single_memo is None:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    return single_memo