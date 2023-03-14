from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_temp = InlineKeyboardButton('Разовое', callback_data='btn_temp')
inline_btn_perm = InlineKeyboardButton('С повторением', callback_data='btn_perm')
inline_btn_book = InlineKeyboardButton('Без даты', callback_data='btn_book')
inline_btn_cancel = InlineKeyboardButton('Отмена', callback_data='btn_cancel')
inline_btn_cancel_adding = InlineKeyboardButton('Отмена', callback_data='cancel_adding')

inline_kb1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_temp, inline_btn_perm).add(inline_btn_book).add(inline_btn_cancel)
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_cancel_adding)

# --- Inline Editing Reminder status buttons ---
inline_btn_done = InlineKeyboardButton('Выполнено', callback_data='btn_done')
inline_btn_delete = InlineKeyboardButton('Удалить', callback_data='btn_delete')
inline_btn_edit = InlineKeyboardButton('Редактировать', callback_data='btn_edit')
inline_btn_back = InlineKeyboardButton('<<< Назад', callback_data='btn_back_list')

inline_kb_edit1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_done,
                                                        inline_btn_delete,
                                                        inline_btn_edit
                                                        )
inline_kb_edit1_back = InlineKeyboardMarkup(row_width=2).add(inline_btn_done,
                                                             inline_btn_delete,
                                                             inline_btn_edit
                                                             ).add(inline_btn_back)

# --- Inline Editing Reminder buttons ---
# inline_btn_back = InlineKeyboardButton('<<< Back', callback_data='btn_back')
inline_btn_edit_text = InlineKeyboardButton('Текст', callback_data='btn_edit_text')
inline_btn_edit_date = InlineKeyboardButton('Дата', callback_data='btn_edit_date')
inline_btn_edit_type = InlineKeyboardButton('Тип', callback_data='btn_edit_type')
inline_btn_edit_frequency = InlineKeyboardButton('Частота', callback_data='btn_edit_frq')

inline_kb_edit2 = InlineKeyboardMarkup(row_width=2).add(inline_btn_edit_text,
                                                        inline_btn_edit_date,
                                                        inline_btn_back)
inline_kb_edit3 = InlineKeyboardMarkup(row_width=2).add(inline_btn_edit_text,
                                                        inline_btn_edit_frequency,
                                                        inline_btn_back)
