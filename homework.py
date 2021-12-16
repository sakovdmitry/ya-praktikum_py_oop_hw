class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:

        # coefficients calories: cc_1, cc_2
        cc_1 = 18
        cc_2 = 20
        speed = self.get_mean_speed()
        weight = self.weight
        time = self.duration * 60
        coeff_time = Training.M_IN_KM

        # formula
        calories = (cc_1 * speed - cc_2) * weight / coeff_time * time

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

    def get_spent_calories(self) -> float:

        # coefficients calories: cc_1, cc_2
        cс_1 = 0.035
        cс_2 = 0.029
        weight = self.weight
        speed = self.get_mean_speed()
        height = self.height
        time = self.duration * 60

        # formula: calories in 1 min * total distance time in minutes
        cal_in_1min = (cс_1 * weight + (speed**2 // height) * cс_2 * weight)
        calories = cal_in_1min * time

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:

        # coefficients
        length = self.length_pool
        count = self.count_pool
        c = Training.M_IN_KM
        duration = self.duration

        # formula
        speed = length * count / c / duration

        return speed

    def get_spent_calories(self) -> float:

        # coefficients calories: cc_1
        cc_1 = 1.1
        weight = self.weight
        speed = self.get_mean_speed()

        # formula
        calories = (speed + cc_1) * 2 * weight

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in type_training:
        Training = type_training[workout_type](*data)
        return Training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
