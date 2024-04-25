import json
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter,Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_to_cart, orm_add_user, orm_get_cart, orm_get_cart_item, orm_get_products, orm_get_user_by_tg, orm_update_cart_item_quantity, orm_update_user  # Italic, as_numbered_list и тд
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from filters.chat_types import ChatTypeFilter


from kbds.reply import get_keyboard

class ChangeProfile(StatesGroup):
    first_name = State()
    last_name = State()
    card_number= State()

    profile_for_change = None



handle_buy_cb_data = 'handle_buy_cb_data'
handle_profile_cb_data = 'handle_profile_cb_data'
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))



@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Hello, wanna buy something?",
        reply_markup=get_keyboard(
            "Catalog",
            "Cart",
            "About",
            "Profile",
            "How we deliver",
            placeholder="What interests you?",
            sizes=(3, 2)
        ),
    )



@user_private_router.message(or_f(Command("profile"), (F.text.lower() == 'profile')))
async def profile_cmd(message: types.Message, session: AsyncSession):
    user = await orm_get_user_by_tg(session=session, tg_id= message.from_user.id)
    if not user:
        info_dict = {
            'telegram_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
        await orm_add_user(session=session,data=info_dict )
        user = await orm_get_user_by_tg(session=session, tg_id= message.from_user.id)


    text = as_list(
        f'first name: {user.first_name}',
        f'last name: {user.last_name}',
        f'telegram id: {user.telegram_id}',
        f'card number: {user.card_number}',
        sep="\n----------------------\n",
    )    
    markup = InlineKeyboardMarkup(inline_keyboard= get_profile_inline_kb())


    await message.answer(text.as_html(), reply_markup=markup)
    
def get_profile_inline_kb():
    
    edit_profile_btn = InlineKeyboardButton(text= 'Edit Profile', callback_data=handle_profile_cb_data )
    rows = [ [edit_profile_btn]]
    return rows

@user_private_router.callback_query(StateFilter(None),F.data.contains( handle_profile_cb_data)  )
async def handle_profile_cb(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext):
    user = await orm_get_user_by_tg(session, callback_query.from_user.id)
    ChangeProfile.profile_for_change= user
    await callback_query.message.answer(
    "Enter your new first name", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(ChangeProfile.first_name)

@user_private_router.message(ChangeProfile.first_name, or_f(F.text, F.text == "."))
async def add_first_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(first_name=ChangeProfile.profile_for_change.first_name)
    else:
        if len(message.text) >= 100:
            await message.answer(
                "The name should be no more than 100 symbols"
            )
            return

        await state.update_data(first_name=message.text)
    await message.answer("Enter your last name")
    await state.set_state(ChangeProfile.last_name)


@user_private_router.message(ChangeProfile.last_name, or_f(F.text, F.text == "."))
async def add_last_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(last_name=ChangeProfile.profile_for_change.last_name)
    else:
        await state.update_data(last_name=message.text)
    await message.answer("Enter your card number")
    await state.set_state(ChangeProfile.card_number)

@user_private_router.message(ChangeProfile.card_number, or_f(F.text, F.text == "."))
async def add_card_number(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(card_number=ChangeProfile.profile_for_change.card_number)
    else:
        await state.update_data(card_number = message.text)
    data = await state.get_data()
    try:
        if ChangeProfile.profile_for_change:
            await orm_update_user(session, ChangeProfile.profile_for_change.id, data)

        await message.answer("User was changed")
        await state.clear()

    except Exception as e:
        await message.answer(
            'error'
        )
        await state.clear()

    ChangeProfile.profile_for_change = None





@user_private_router.message(or_f(Command("catalog"), (F.text.lower().contains("catalog"))))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        markup = InlineKeyboardMarkup(inline_keyboard= get_product_inline_kb(product.id))
        
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nPrice: {round(product.price, 2)}",reply_markup= markup
        )


@user_private_router.message(or_f(Command("cart"), (F.text.lower().contains("cart"))))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for items in await orm_get_cart(session, message.from_user.id):
        
        await message.answer_photo(
            items.product.image,
            caption=f"<strong>{items.product.name}\
                    </strong>\n{items.product.description}\nPrice: {round(items.product.price, 2)}\nQuantity: {items.quantity}"
        )



def get_product_inline_kb(product_id):
    callback_btn = InlineKeyboardButton(text= 'buy', callback_data=handle_buy_cb_data +f'_{product_id}')
    rows = [  [callback_btn]]
    return rows

@user_private_router.callback_query(F.data.contains( handle_buy_cb_data)  )
async def handle_buy_cb(callback_query: CallbackQuery, session: AsyncSession):
    arr_w= callback_query.data.split("_")
    product_id = int(arr_w[len(arr_w)-1])
    user =  await orm_get_user_by_tg(session,callback_query.from_user.id)
    if not user:
        await callback_query.answer(text = f'No user Existing')
        return 
    cart_items = await orm_get_cart_item(session, user.id, product_id)
    if not cart_items:
        await orm_add_to_cart(session, user_id=user.id, product_id=product_id, quantity=1)
    else:
        await orm_update_cart_item_quantity(session, cart_items[0].id, cart_items[0].quantity+1)

    await callback_query.answer(text = f'Product Added to Cart Successfully')



@user_private_router.message(F.text.lower() == "about")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    text = as_list(
            "We have been around 30 years on the market",
            "We sell good food and beverages",
            "100% natural",

            sep="\n",
        )
    await message.answer(text.as_html())




@user_private_router.message(
    (F.text.lower().contains("deliver")) | (F.text.lower() == "your delivery"))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("We can"),
            "Somebody will come and take it",
            "Come and get it",
            "I'll eat on the run",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("We can't:"),
            "deliver to your relatives",
            "deliver by train",
            marker="❌ "
        ),
        sep="\n",
    )
    await message.answer(text.as_html())


