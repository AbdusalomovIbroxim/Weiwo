from sqlalchemy import Column, Integer, String, select

from database import Base, db


class User_In_Company(Base):
    telegram_id = Column(String)
    company_id = Column(Integer)
    type = Column(String(30))

    def __repr__(self):
        return f'<{self.__class__.__name__:} pk={self.pk}, company_id={self.company_id}, type={self.type}'

    @classmethod
    async def add_staff_(cls, telegram_id: str, **kwargs: str):
        query = cls(telegram_id=telegram_id, **kwargs)
        db.add(query)
        await cls.commit()
        return query

    @classmethod
    async def is_staff(cls, staff_id: str, company_id: int):
        staffs = cls.staff_list(company_id)
        result = await staffs
        return bool((staff_id,) is result)

    @classmethod
    async def staff_list(cls, company_id, type_: str = None) -> len:
        if type_:
            query = select(cls.telegram_id).where(
                cls.company_id == company_id, cls.type == type_)
        else:
            query = select(cls.telegram_id).where(
                cls.company_id == company_id)
        staffs = await db.execute(query)
        user, = staffs.fetchall() or None,
        return user
