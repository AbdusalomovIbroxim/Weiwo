from datetime import datetime

from sqlalchemy import Column, Integer, String, update, delete, Date
from sqlalchemy.future import select

from aiobot.database import Base, db


class User(Base):
    user_id = Column(String(50), unique=True)
    full_name = Column(String(30))
    phone_number = Column(String(30))
    score = Column(Integer, default=10)
    lang = Column(String(2))
    status = Column(String, default='user')
    created_at = Column(Date, default=datetime.now())

    def __repr__(self):
        return f'<{self.__class__.__name__:} pk={self.pk}, user_id={self.user_id}, full_name={self.full_name}, status={self.status}>'

    @classmethod
    async def create(cls, user_id, **kwargs):
        user = cls(user_id=user_id, **kwargs)  # noqa
        db.add(user)
        await cls.commit()
        return user

    @classmethod
    async def get(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        users = await db.execute(query)
        user, = users.first() or None,
        return user

    @classmethod
    async def get_all(cls):
        query = select(cls)
        users = await db.execute(query)
        return users

    @classmethod
    async def update(cls, user_id, **kwargs):
        query = (
            update(cls)
            .where(cls.user_id == user_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def delete(cls, user_id):
        query = delete(cls).where(cls.user_id == user_id)
        await db.execute(query)
        await cls.commit()
        return True

    @classmethod
    async def get_lang(cls, user_id: str):
        query = select(cls.lang).where(cls.user_id == user_id)
        langs = await db.execute(query)
        lang, = langs
        return lang[0]

    @classmethod
    async def check_admin(cls, user_id: str) -> bool:
        query = select(cls.status).where(cls.user_id == user_id)
        statutes = await db.execute(query)
        status, = statutes
        return status[0]

    @classmethod
    async def tell(cls, user_id: str):
        query = select(cls.phone_number).where(cls.user_id == user_id)
        phone_number = await db.execute(query)
        number, = phone_number
        return number[0]
