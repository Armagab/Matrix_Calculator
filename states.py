from aiogram.dispatcher.filters.state import StatesGroup, State


class Condition(StatesGroup):
    InputRows = State()
    InputColumns = State()
    InputMatrix = State()
    WaitForChoice = State()
    NextMatrixSum = State()
    NextMatrixMult = State()
    Continue = State()
    Power = State()
