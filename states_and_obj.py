from aiogram.dispatcher.filters.state import State, StatesGroup

from scripts import get_user_by_id


# Класс состояний формы
class Form(StatesGroup):
    name, age, sex, personal_data, img, start_registration = State(), State(), State(), State(), State(), State()


class Form1(StatesGroup):
    image = State()


class Form2(StatesGroup):
    text = State()


class Profile:
    def __init__(self, user_id):
        self.profile = get_user_by_id(user_id)


class User(Profile):
    def __init__(self, user_id):
        super().__init__(user_id)
        if hasattr(self, 'profile'):
            self.name = self.profile[0]
            self.user_id = self.profile[1]
            self.age = self.profile[2]
            self.sex = self.profile[3]
            self.personal_data = self.profile[4]
            self.chat_id = self.profile[5]
            self.index = self.profile[6]
            self.index_like = self.profile[7]
            self.index_activity = self.profile[8]
            self.photo = self.profile[9]
