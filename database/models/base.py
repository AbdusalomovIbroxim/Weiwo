from datetime import datetime

from sqlalchemy import Column, String, Date, select, update, delete

from database import Base, db


class Product(Base):
    telegram_id = Column(String(50))
    full_name = Column(String(30))
    city = Column(String)
    name = Column(String)
    category = Column(String)
    sub_category = Column(String)
    yandex_maps_url = Column(String)
    photo = Column(String)
    description = Column(String)
    explanation = Column(String)
    created_at = Column(Date, default=datetime.now())

    def __repr__(self):
        return f'<{self.__class__.__name__:} pk={self.pk}, telegram_id={self.telegram_id},' \
               f'full_name={self.full_name}, city={self.city}, name={self.name}, category={self.category},' \
               f'sub_category={self.sub_category}, yandex_maps_url={self.yandex_maps_url},' \
               f'photo={self.photo}, description={self.description}, explanation={self.explanation}>'

    @classmethod
    async def add_product(cls, user_id, **kwargs):
        product = cls(telegram_id=user_id, **kwargs)
        db.add(product)
        await cls.commit()
        return product

    @classmethod
    async def get(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        users = await db.execute(query)
        user, = users.first() or None,
        return user

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
    async def get_company_names(cls, city, category, sub_category):
        query = select(cls.name).where(
            Product.city == city and Product.category == category and Product.sub_category == sub_category)
        names = await db.execute(query)
        return names

    @classmethod
    async def get_company(cls, **kwargs):
        query = select(cls).where(**kwargs)
        companyes = await db.execute(query)
        return companyes
