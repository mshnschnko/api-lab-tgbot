from aiogram.dispatcher.filters.state import StatesGroup, State


class FormTemp(StatesGroup):
    title = State()
    date = State()
    attachments = State()


class FormPerm(StatesGroup):
    title = State()
    date = State()
    frequency = State()
    attachments = State()


class FormBookmark(StatesGroup):
    title = State()
    attachments = State()

class Edit(StatesGroup):
    id = State()
    title = State()
    date = State()
    attachments = State()