from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from database.models import Cart, Product, User


async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Product).where(Product.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()




async def orm_add_user(session: AsyncSession, data: dict):
    new_user = User(
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        card_number=data.get("card_number"),
        telegram_id=data['telegram_id']
    )
    session.add(new_user)
    await session.commit()

async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_user_by_tg(session: AsyncSession, tg_id: int):
    query = select(User).where(User.telegram_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user(session: AsyncSession, user_id: int, data: dict):
    query = update(User).where(User.id == user_id).values(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        card_number=data.get("card_number")
    )
    await session.execute(query)
    await session.commit()

async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()



async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int, quantity: int):
    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    session.add(cart_item)
    await session.commit()



async def orm_get_cart(session: AsyncSession, telegram_id: int):
    user = await orm_get_user_by_tg(session, telegram_id)
    query = select(Cart).where(Cart.user_id == user.id).options(joinedload(Cart.product))
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_cart_item(session: AsyncSession, user_id: int, product_id :int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_cart_item_quantity(session: AsyncSession, cart_item_id: int, quantity: int):
    query = update(Cart).where(Cart.id == cart_item_id).values(quantity=quantity)
    await session.execute(query)
    await session.commit()

async def orm_delete_cart_item(session: AsyncSession, cart_item_id: int):
    query = delete(Cart).where(Cart.id == cart_item_id)
    await session.execute(query)
    await session.commit()
