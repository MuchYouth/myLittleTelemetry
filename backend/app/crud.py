from sqlalchemy.orm import Session
from . import models

def create_or_update_yml(db: Session, filename: str, path: str):
    # 1) 같은 filename 레코드가 있나 찾아서
    db_obj = db.query(models.YMLFile).filter(models.YMLFile.filename == filename).first()
    if db_obj:
        # 2a) 있으면 path만 덮어쓰기
        db_obj.path = path
        # (원한다면 updated_at도 직접 바꾼 뒤에)
    else:
        # 2b) 없으면 새로 생성
        db_obj = models.YMLFile(filename=filename, path=path)
        db.add(db_obj)

    db.commit()
    db.refresh(db_obj)
    return db_obj
