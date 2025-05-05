from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class YMLFile(Base):
    __tablename__ = "yaml_files"   # MySQL에 이미 만드신 테이블 이름과 일치시켜 주세요
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True, nullable=False)
    path = Column(String(512), nullable=False)   # 업로드된 파일의 저장 경로
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
