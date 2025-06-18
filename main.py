import asyncio
from models import UsersOrm, GendersORM
from database_engine import Base, async_engine, make_async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База сброшена")

async def gender_run():
    async with make_async_session() as session:
        gender = [GendersORM(gender='Male'), GendersORM(gender='Female')]
        session.add_all(gender)
        await session.commit()
        # print("✅ Добавлен пол:", gender.gender)

async def create_users():
    async with make_async_session() as session:
        # Создаём родителей
        mother = UsersOrm(name="Мама", age=40, gender_id=2)
        father = UsersOrm(name="Папа", age=42, gender_id=1)
        session.add_all([mother, father])
        await session.flush()  # Получим id до коммита

        # Создаём ребёнка
        child = UsersOrm(
            name="Ребёнок",
            age=10,
            gender_id=1,
            mother_id=mother.id,
            father_id=father.id
        )
        session.add(child)
        await session.commit()
        print("✅ Пользователи добавлены")

async def select_data():
    async with make_async_session() as session:
        stmt = (
            select(UsersOrm)
            .options(
                selectinload(UsersOrm.children_as_mother),
                selectinload(UsersOrm.children_as_father)
            )
            .where(UsersOrm.name == "Мама")
        )
        result = await session.execute(stmt)
        mother = result.scalars().first()

        print(f"🧑‍🍼 Мама: {mother.name}")
        for child in mother.children_as_mother:
            print(f"  → Ребёнок: {child.name}, возраст: {child.age}")

async def main():
    await reset_db()
    await gender_run()
    await create_users()
    await select_data()

asyncio.run(main())
