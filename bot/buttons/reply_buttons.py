from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- utils buttons ---
btnBack = KeyboardButton('Назад')
btnCancel = KeyboardButton('Отмена')
btnCleanDone = KeyboardButton('Очистить')

cancelMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)

# --- Main Menu buttons ---
btnCreate = KeyboardButton('Создать новое')
btnWatchList = KeyboardButton('Показать напоминания')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(btnCreate,
                                                                                              btnWatchList,
                                                                                              btnCleanDone)

# --- Show Reminders Menu buttons ---
btnShowAll = KeyboardButton('Все')
btnShowPermanent = KeyboardButton('С повторением')
btnShowTemporary = KeyboardButton('Разовое')
btnShowBookmarks = KeyboardButton('Без даты')
remindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnShowAll,
                                                                           btnShowPermanent,
                                                                           btnShowTemporary,
                                                                           btnShowBookmarks,
                                                                           btnBack)

# --- Reminders Menu buttons ---
anyRemindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnCleanDone, btnBack)
