from aiogram.dispatcher import FSMContext
from aiogram import types
from config import admin_id
from keyboards import kb_client, kb_client_2, kb_client_3, kb_client_4
from main import bot, dp
from states import Condition
from algorithms import *


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Bot has started")


@dp.message_handler(commands=["start"], state='*')
async def start_command(message: types.Message, state: FSMContext):
    await message.reply("Это матричный калькулятор. Для начала работы с матрицей введите /matrix")
    await state.reset_state()
    await state.reset_data()


@dp.message_handler(commands=["reset"], state='*')
async def start_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.reset_data()
    await message.answer("Введите количество строк и столбцов вашей матрицы.")
    await message.answer("Количество строк:")

    await state.update_data(operation="start")

    await Condition.InputRows.set()


@dp.message_handler(commands=["matrix"])
async def start_matrix_operations(message: types.Message, state: FSMContext):
    await message.answer("Введите количество строк и столбцов вашей матрицы.")
    await message.answer("Количество строк:")

    await state.update_data(operation="start")

    await Condition.InputRows.set()


@dp.message_handler(state=Condition.InputRows)
async def rows_input(message: types.Message, state: FSMContext):
    try:
        await state.update_data(last_rows=int(message.text))

        data = await state.get_data()
        if data["operation"] == "start":
            await state.update_data(first_rows=int(message.text))
            await state.update_data(prev_rows=int(message.text))
            await state.update_data(det="uknown")
        await Condition.InputColumns.set()
        await message.answer("Количество столбцов:")

    except Exception:
        await message.answer("Ошибка, введите целое число.")
        await message.answer("Количество строк:")

        await state.update_data(operation="start")

        await Condition.InputRows.set()


@dp.message_handler(state=Condition.InputColumns)
async def columns_input(message: types.Message, state: FSMContext):
    try:
        await state.update_data(last_columns=int(message.text))

        data = await state.get_data()
        if data["operation"] == "start":
            await state.update_data(first_columns=int(message.text))
            await state.update_data(prev_columns=int(message.text))

        size = str(data["last_rows"]) + "x" + str(data["last_columns"])
        await message.answer(size)

        await Condition.InputMatrix.set()
        await message.answer("Вводите элементы матрицы через пробел (Можете просто одной "
                             "строкой, "
                             "но если хотите перенести на другую строку без отправления "
                             "- Shift + Enter)")
    except Exception:
        await message.answer("Ошибка, введите целое число.")
        await message.answer("Количество столбцов:")

        await Condition.InputColumns.set()


@dp.message_handler(state=Condition.InputMatrix)
async def matrix_input(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        if data["last_rows"] == 1 and data["last_columns"] == 1:
            await message.answer("С такими недоматрицами не работаем, введите /reset и введите матрицу с "
                                 "минимум двумя элементами")
        last_matrix = create_matrix(data["last_rows"], data["last_columns"], message.text)
        if data["operation"] == "start":
            await state.update_data(last_matrix=last_matrix)
            await state.update_data(first_matrix=last_matrix)
            await state.update_data(prev_matrix=last_matrix)

            await message.answer("Ваша матрица <b><i>M</i></b>:")
            await message.answer(matrix_output(last_matrix))

            await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                                   reply_markup=kb_client)

            await Condition.WaitForChoice.set()

        elif data["operation"] == "multiplication":
            await state.update_data(last_matrix=last_matrix)
            data = await state.get_data()

            await message.answer("Ваши матрицы:")
            await message.answer(matrix_output(data["prev_matrix"]))
            await message.answer("x")
            await message.answer(matrix_output(last_matrix))
            await message.answer("=")
            result = matrix_multiplication(data["prev_matrix"], data["last_matrix"])
            await message.answer(matrix_output(result))

            await state.update_data(last_matrix=result)
            await state.update_data(last_rows=len(result))
            await state.update_data(last_columns=len(result[0]))

            await Condition.Continue.set()
            await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                                   reply_markup=kb_client_2)

        elif data["operation"] == "sum":
            await state.update_data(last_matrix=last_matrix)
            data = await state.get_data()

            await message.answer("Ваши матрицы:")
            await message.answer(matrix_output(data["prev_matrix"]))
            await message.answer(data["sum_oper"])
            await message.answer(matrix_output(last_matrix))
            await message.answer("=")
            result = matrix_sum(data["prev_matrix"], data["last_matrix"], data["sum_oper"])
            await message.answer(matrix_output(result))
            await state.update_data(last_matrix=result)

            await Condition.Continue.set()
            await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                                   reply_markup=kb_client_2)
    except Exception:
        data = await state.get_data()
        size = str(data["last_rows"]) + "x" + str(data["last_columns"])
        await message.answer(f"Ошибка! Введите матрицу размером {size}")
        await Condition.InputMatrix.set()


@dp.message_handler(commands=["Жорданова"], state=Condition.WaitForChoice)
async def jordan_out(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()

        ans = jordan_normal_form(data["last_matrix"])
        P, J = ans[0], ans[1]

        await message.answer("Матрица преобразования <b><i>P</i></b>:")
        await message.answer(matrix_output(P))
        P = matrix_to_array(P)
        await state.update_data(P=P)

        await message.answer("Жорданова Форма <b><i>J</i></b>:")
        await message.answer(matrix_output(J))
        await message.answer("Где <b><i>M = P * J * P^(-1).</i></b>")
        J = matrix_to_array(J)
        await state.update_data(last_matrix=J)

        await Condition.Continue.set()
        await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                               reply_markup=kb_client_2)
    except Exception:
        data = await state.get_data()
        await message.answer("Ошибка!")
        await message.answer("Жорданову Форму можно найти только у квадратной матрицы.")
        await message.answer("Ваша матрица <b><i>M</i></b>:")
        await message.answer(matrix_output(data["last_matrix"]))

        await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                               reply_markup=kb_client)
        await Condition.WaitForChoice.set()


@dp.message_handler(commands=["Определитель"], state=Condition.WaitForChoice)
async def det(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer_exists = 1
    if data["last_rows"] == 2 and data["last_columns"] == 2:
        matrix = data["last_matrix"]
        await message.answer("Определитель считается просто:")
        result = determinant(data["last_matrix"])
        await message.answer(f"({matrix[0][0]} * {matrix[1][1]}) - ({matrix[1][0]} * {matrix[0][1]}) = {result}")
    else:
        await message.answer("Найдем определитель методом Гаусса")
        dividers = []
        column = 0
        matrix = data["last_matrix"][:]
        all_nulls = 0
        minus = False
        while column < len(matrix[0]):
            for row in matrix:
                row2 = intify_arr(row)
                if row2.count(0) == len(row2):
                    await message.answer("Найдена нулевая строка!")
                    all_nulls = 1
                    break
            if all_nulls:
                break
            await message.answer("Ищем максимальный по модулю элемент в {0}-м столбце:".format(column + 1))
            current_row = None
            for r in range(column, len(matrix)):
                if current_row is None or abs(matrix[r][column]) > abs(matrix[current_row][column]):
                    current_row = r
            if current_row is None:
                await message.answer("Решений нет.")
                answer_exists = 0
                break
            await message.answer(matrix_output(matrix))
            if current_row != column:
                await message.answer("Переставляем строку с найденным элементом повыше:")
                swap_rows(matrix, current_row, column)
                minus = 1 - minus
                await message.answer(matrix_output(matrix))
            if not all_nulls:
                await message.answer("Нормализуем строку с найденным элементом:")
                dividers.append(round(matrix[column][column], 2))
                divide_row(matrix, column, matrix[column][column])
                await message.answer(matrix_output(matrix))
                await message.answer("Обрабатываем нижележащие строки:")
                for r in range(column + 1, len(matrix)):
                    combine_rows(matrix, r, column, -matrix[r][column])
                await message.answer(matrix_output(matrix))
                column += 1
        if answer_exists:
            if all_nulls:
                await message.answer("Если есть нулевая строка или столбец, определитель матрицы равен нулю.")
                data["det"] = 0
                result = 0
            else:
                await message.answer("Матрица приведена к треугольному виду")
                await message.answer("Приведенная к единичному виду матрица:")
                await message.answer(matrix_output(matrix))
                await message.answer("Делители:")
                await message.answer(output_array(dividers))
                await message.answer("Считаем определитель, перемножая все элементы в списке делителей и меняя его "
                                     "знак за каждую перестановку строк.")
                result = str(round(-1 * multiply_array(dividers), 6)) if minus else str(
                    round(multiply_array(dividers), 6))
    if answer_exists:
        await message.answer("Определитель равен:")
        await message.answer(result)
    if data["operation"] == "Inverse":
        if data["det"] == 0:
            await message.answer("Определитель равен нулю, обратную матрицу найти невозможно.")
            await message.answer("Ваша матрица <b><i>M</i></b>:")
            await message.answer(matrix_output(data["last_matrix"]))

            await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                                   reply_markup=kb_client)
        else:
            await message.answer("Определитель не равен нулю, найдем обратную матрицу")
            await message.answer("Исходная матрица:")
            await message.answer(matrix_output(data["last_matrix"]))
            result = inverse_matrix(data["last_matrix"])
            await message.answer("Обратная матрица:")
            await message.answer(matrix_output(result))
            await state.update_data(last_matrix=result)
            await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                                   reply_markup=kb_client_2)
            await Condition.Continue.set()
    else:
        await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                               reply_markup=kb_client_3)
        await Condition.Continue.set()


@dp.message_handler(commands=["Умножение"], state=Condition.WaitForChoice)
async def jordan_out(message: types.Message, state: FSMContext):
    await state.update_data(operation="multiplication")
    data = await state.get_data()
    await bot.send_message(message.from_user.id, text="Введите количество строк и столбцов второй матрицы.")
    rows = data["last_columns"]
    await bot.send_message(message.from_user.id, text=f"Количество строк = {rows} (столько же, сколько столбцов в "
                                                      f"умножаемой матрице)")
    await state.update_data(last_rows=rows)
    await Condition.InputColumns.set()
    await message.answer("Количество столбцов:")


@dp.message_handler(commands=["Сумма"], state=Condition.WaitForChoice)
async def jordan_out(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Вводите элементы второй матрицы с таким же размером")

    size = str(data["last_rows"]) + "x" + str(data["last_columns"])
    await message.answer(size)

    await state.update_data(operation="sum")
    await state.update_data(sum_oper="+")
    await Condition.InputMatrix.set()


@dp.message_handler(commands=["Вычитание"], state=Condition.WaitForChoice)
async def jordan_out(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Вводите элементы второй матрицы с таким же размером")

    size = str(data["last_rows"]) + "x" + str(data["last_columns"])
    await message.answer(size)

    await state.update_data(operation="sum")
    await state.update_data(sum_oper="-")
    await Condition.InputMatrix.set()


@dp.message_handler(commands=["Обратная"], state=Condition.WaitForChoice)
async def jordan_out(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        if data["last_rows"] != data["last_columns"]:
            await message.answer("Ошибка!")
            await message.answer("Обратную матрицу можно найти только у квадратных матриц.")
            await message.answer("Ваша матрица <b><i>M</i></b>:")
            await message.answer(matrix_output(data["last_matrix"]))

            await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                                   reply_markup=kb_client)
            await Condition.WaitForChoice.set()
        else:
            await state.update_data(operation="Inverse")
            await bot.send_message(message.from_user.id, text="Проверим, равен ли нулю определитель",
                                   reply_markup=kb_client_4)
    except Exception:
        data = await state.get_data()
        await message.answer("Ошибка!")
        await message.answer("Обратную матрицу можно найти только у квадратных матриц.")
        await message.answer("Ваша матрица <b><i>M</i></b>:")
        await message.answer(matrix_output(data["last_matrix"]))

        await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                               reply_markup=kb_client)
        await Condition.WaitForChoice.set()


@dp.message_handler(commands=["Возвести"], state=Condition.WaitForChoice)
async def in_power(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data["last_rows"] == data["last_columns"]:
        await message.answer("В какую степень вы хотите возвести матрицу?")
        await Condition.Power.set()
    else:
        rows = data["last_rows"]
        columns = data["last_columns"]
        await message.answer("Ошибка!")
        await message.answer("Возводить в степень можно только квадратные матрицы")
        await message.answer(f"Так как иначе, в вашем случае, пришлось бы "
                             f"умножить матрицу {rows}x{columns} на матрицу {rows}x{columns}, что невозможно.")
        await message.answer("Ваша матрица <b><i>M</i></b>:")
        await message.answer(matrix_output(data["last_matrix"]))

        await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                               reply_markup=kb_client)
        await Condition.WaitForChoice.set()


@dp.message_handler(state=Condition.Power)
async def in_power_next(message: types.Message, state: FSMContext):
    await state.update_data(power=int(message.text))
    data = await state.get_data()
    result = white_power(data["last_matrix"], data["power"])
    await state.update_data(prev_matrix=data["last_matrix"])
    await state.update_data(last_matrix=result)
    await message.answer(matrix_output(result))
    await Condition.Continue.set()
    await bot.send_message(message.from_user.id, text="С какой матрицей работаем дальше?",
                           reply_markup=kb_client_2)


@dp.message_handler(commands=["Исходная"], state=Condition.Continue)
async def jordan_out(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await state.update_data(last_rows=data["first_rows"])
    await state.update_data(last_columns=data["first_columns"])
    await state.update_data(last_matrix=data["first_matrix"])
    await state.update_data(prev_rows=data["first_rows"])
    await state.update_data(prev_columns=data["first_columns"])
    await message.answer("Ваша матрица:")
    await message.answer(matrix_output(data["first_matrix"]))

    await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                           reply_markup=kb_client)
    await Condition.WaitForChoice.set()


@dp.message_handler(commands=["Предыдущая"], state=Condition.Continue)
async def jordan_out(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await state.update_data(last_rows=data["prev_rows"])
    await state.update_data(last_columns=data["prev_columns"])
    await state.update_data(last_matrix=data["prev_matrix"])
    await message.answer("Ваша матрица:")
    await message.answer(matrix_output(data["prev_matrix"]))

    await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                           reply_markup=kb_client)
    await Condition.WaitForChoice.set()


@dp.message_handler(commands=["Продолжаем"], state=Condition.Continue)
async def jordan_out(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(prev_rows=data["last_rows"])
    await state.update_data(prev_columns=data["last_columns"])
    await state.update_data(prev_matrix=data["last_matrix"])

    await message.answer("Ваша матрица:")
    await message.answer(matrix_output(data["last_matrix"]))

    await bot.send_message(message.from_user.id, text="Какое действие вы хотели бы с ней произвести?",
                           reply_markup=kb_client)
    await Condition.WaitForChoice.set()
