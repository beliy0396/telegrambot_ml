from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    get_area = State()
    get_floor_max = State()
    get_floor = State()
    get_rooms_count = State()
    get_extra_area_type_name = State()
    get_hot_water = State()

