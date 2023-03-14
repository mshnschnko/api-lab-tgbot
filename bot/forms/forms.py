from aiogram.dispatcher.filters.state import StatesGroup, State


class FormTemp(StatesGroup):
    title = State()
    date = State()


class FormPerm(StatesGroup):
    title = State()
    date = State()
    frequency = State()


class FormBookmark(StatesGroup):
    title = State()
