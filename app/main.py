from fastapi import FastAPI, HTTPException
from app.schemas import MemoCreate, MemoResponse
from datetime import datetime

app = FastAPI()

# Temporal
memos = []
next_id = 1

@app.post("/memos")
def create_memo(memo: MemoCreate) -> MemoResponse:
    global next_id

    response = MemoResponse(
        id=next_id,
        title=memo.title,
        content=memo.content,
        created_at=datetime.now()
    )
    memos.append(response.model_dump())

    next_id += 1

    return response

@app.get("/memos")
def get_memos() -> list[MemoResponse]:
    return memos

@app.get("/memos/{memo_id}")
def get_memo(memo_id: int) -> MemoResponse:
    for single_memo in memos:
        if single_memo["id"] == memo_id:
            return single_memo
    raise HTTPException(status_code=404, detail="Memo not found")

@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoCreate) -> MemoResponse:
    for single_memo in memos:
        if single_memo["id"] == memo_id:
            single_memo["title"] = memo.title
            single_memo["content"] = memo.content
            return single_memo

    raise HTTPException(status_code=404, detail="Memo not found")

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    for single_memo in memos:
        if single_memo["id"] == memo_id:
            memos.remove(single_memo)
            return
    raise HTTPException(status_code=404, detail="Memo not found")