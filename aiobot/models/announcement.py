from sqlalchemy import Column, String, select, update

from aiobot.database import Base, db


class Announcement(Base):
    user_id = Column(String)
    type = Column(String)
    phone_number = Column(String)
    photo = Column(String)
    description = Column(String)
    category = Column(String)
    sub_category = Column(String)

    def __repr__(self):
        return f'<{self.__class__.__name__:} pk={self.pk}, type={self.type}, phone_number={self.phone_number},' \
               f'photo={self.photo}, description={self.description}, category={self.category}, sub_category={self.sub_category}'

    @classmethod
    async def add(cls, user_id: str, **kwargs):
        announcement = cls(user_id=user_id, **kwargs)
        db.add(announcement)
        await cls.commit()
        return announcement

    @classmethod
    async def get_all(cls):
        query = select(cls)
        announcements = await db.execute(query)
        return announcements

    @classmethod
    async def remove(cls, user_id, phone_number, photo, description, category, sub_category):
        ...

    @classmethod
    async def edit(cls, announcement_id, **kwargs):
        query = (update(cls).where(cls.pk == announcement_id).values(**kwargs))
        await db.execute(query)
        await cls.commit()


"""
type
phone_number
photo
description
category
sub_category
"""
