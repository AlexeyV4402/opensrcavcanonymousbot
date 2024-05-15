from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    Age = State()
    Gender = State()


class SelectRoom(StatesGroup):
    Region = State()
    Room = State()
    Gender = State()
