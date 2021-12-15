class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return(f'Тип тренировки: {self.training_type}; '
              f'Длительность: {self.duration} ч.; '
              f'Дистанция: {self.distance} км; '
              f'Ср. скорость: {self.speed} км/ч; '
              f'Потрачено ккал: {self.calories}.)')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self)
        return training_info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        cc_1 = 18
        cc_2 = 20
        calories = (cc_1 * self.get_mean_speed() - cc_2) * self.weight / Training.M_IN_KM * self.duration
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        cc_1 = 0.035
        cc_2 = 0.029
        calories = (cc_1 * self.weight + (self.get_mean_speed()**2 // self.height) * cc_2 * self.weight) * self.duration
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    
    Training.LEN_STEP = 1.38
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        speed = self.length_pool * self.count_pool / Training.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        cc_1 = 1.1
        calories = (self.get_mean_speed() + cc_1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in type_training:
        Training = type_training[workout_type](data)
    return Training


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info()
    print(info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
