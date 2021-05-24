class Dictionary_State_Store:

    store = {}

    def __init__(self) -> None:
        pass

    def get_state(self, user_id:str) -> None:
        return self.store[user_id]

    def update_state(self, user_id:str, dictionary:dict) -> None:
        self.store[user_id] = dictionary

    def del_state(self, user_id:str) -> dict:
        return self.store.pop(user_id, None)

    def add_state(self, user_id:str) -> None:
        self.store[user_id] = {}

    def user_id_exist(self, user_id:str) -> None:
        if user_id in self.store:
            return True
        else:
            return False
