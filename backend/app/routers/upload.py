from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from .. import models, crud, schemas
from fastapi.responses import RedirectResponse
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ① APIRouter 인스턴스 생성
router = APIRouter()

# ② 데이터베이스 세션 종결 핸들러
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload-yml", summary="YML 파일 업로드")
async def upload_yml(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 확장자 검사 생략...
    content = await file.read()

    # 1) 디스크에 저장
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(content)

    # 2) DB에 기록
    db_obj = crud.create_or_update_yml(
        db,
        filename=file.filename,
        path=save_path
    )

    # 3) 업로드 후 리다이렉트
    return RedirectResponse(url="/html/result.html", status_code=303)


