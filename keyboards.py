from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Объявляем названия кнопок для простоты использования бота
Jordan = KeyboardButton('/Жорданова Форма')
Determinant = KeyboardButton('/Определитель')
Multiplication = KeyboardButton('/Умножение матриц')
Summ = KeyboardButton('/Сумма с другой матрицей')
NegativeSumm = KeyboardButton('/Вычитание другой матрицы из исходной')
Inverse = KeyboardButton('/Обратная матрица')
Power = KeyboardButton('/Возвести в степень')
StartMatrix = KeyboardButton('/Исходная')
PrevMatrix = KeyboardButton('/Предыдущая')
ResultMatrix = KeyboardButton('/Продолжаем с этой')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(Jordan, Determinant, Multiplication, Summ, NegativeSumm, Inverse, Power)

kb_client_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_2.add(StartMatrix, PrevMatrix, ResultMatrix)

kb_client_3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_3.add(StartMatrix, PrevMatrix)

kb_client_4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_4.add(Determinant)
