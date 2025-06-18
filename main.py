import asyncio
from models import UsersOrm, ParentsOrm, GendersORM
from database_engine import Base, async_engine, make_async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База сброшена")


async def gender_run():
    async with make_async_session() as session:
        genders = [
            GendersORM(gender="Male"),
            GendersORM(gender="Female")
        ]
        session.add_all(genders)
        await session.commit()
    print("✅ Полы добавлены")


async def create_users_with_parents():
    async with make_async_session() as session:
        # создаём мать и отца
        mom = UsersOrm(name="Мама", age=40, gender_id=2)
        dad = UsersOrm(name="Папа", age=42, gender_id=1)
        session.add_all([mom, dad])
        await session.flush()

        # создаём ребёнка
        child = UsersOrm(name="Ребёнок", age=10, gender_id=1)
        session.add(child)
        await session.flush()

        # создаём запись в parents
        parents = ParentsOrm(user_id=child.id, mother_id=mom.id, father_id=dad.id)
        session.add(parents)

        await session.commit()
    print("✅ Пользователи и родители добавлены")


async def show_user_and_parents(user_id: int):
    async with make_async_session() as session:
        stmt = (
            select(UsersOrm)
            .options(
                selectinload(UsersOrm.parents).selectinload(ParentsOrm.mother),
                selectinload(UsersOrm.parents).selectinload(ParentsOrm.father),
            )
            .where(UsersOrm.id == user_id)
        )
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            print("Пользователь не найден")
            return

        print(f"\n👤 Пользователь: {user.name}, возраст: {user.age}")
        if user.parents:
            if user.parents.mother:
                print(f"👩 Мать: {user.parents.mother.name}, возраст: {user.parents.mother.age}")
            else:
                print("👩 Мать: не указана")

            if user.parents.father:
                print(f"👨 Отец: {user.parents.father.name}, возраст: {user.parents.father.age}")
            else:
                print("👨 Отец: не указан")
        else:
            print("⚠️ У пользователя нет связанной записи в таблице parents")


async def main():
    # await reset_db()
    # await gender_run()
    # await create_users_with_parents()
    await show_user_and_parents(user_id=1)  # ID ребёнка

asyncio.run(main())
