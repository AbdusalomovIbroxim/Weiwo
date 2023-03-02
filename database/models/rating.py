from sqlalchemy import Column, Integer, String, select

from database import Base, db


class UserInCompany(Base):
    telegram_id = Column(Integer)
    company_id = Column(Integer)
    type = Column(String(30))

    def __repr__(self):
        return f'<{self.__class__.__name__:} pk={self.pk}, company_id={self.company_id}, type={self.type}'

    @classmethod
    async def add_staff_(cls, **kwargs):
        query = cls(**kwargs)
        db.add(query)
        await cls.commit()
        return query

    @classmethod
    async def is_staff(cls, staff_id, company_id):
        staffs = UserInCompany.staff_list(company_id)
        return (staff_id,) in staffs

    @classmethod
    async def staff_list(cls, company_id, type_: str = None):
        if type_:
            query = select(UserInCompany.telegram_id).where(
                UserInCompany.company_id == company_id and UserInCompany.type == type_)
        else:
            query = select(UserInCompany.telegram_id).where(
                UserInCompany.company_id == company_id)
        return await db.execute(query)
