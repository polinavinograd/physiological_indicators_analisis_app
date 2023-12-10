class User:
    def __init__(self, user_id: str, weight: int, height: int, age: int, sex: bool = None, brm: float = None):
        self.name = user_id
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex
        if sex is not None:
            self.brm = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age) if not sex \
                else 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            self.brm = brm
