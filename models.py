from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String(50), primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    published_at = Column(TIMESTAMP, nullable=False)
    thumbnail_url = Column(String(50))

    def __repr__(self):
        return f"<Video(video_id='{self.video_id}', title='{self.title}', description='{self.description}', published_at='{self.published_at}', thumbnail_url='{self.thumbnail_url}')>"