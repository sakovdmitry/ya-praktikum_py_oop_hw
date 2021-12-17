from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    text_training_type = 'Тип тренировки'
    text_duration = 'Длительность'
    text_distance = 'Дистанция'
    text_speed = 'Ср. скорость'
    text_calories = 'Потрачено ккал'

    def get_message(self) -> str:
        return (f'{self.text_training_type}: {self.training_type}; '
                f'{self.text_duration}: {self.duration:.3f} ч.; '
                f'{self.text_distance}: {self.distance:.3f} км; '
                f'{self.text_speed}: {self.speed:.3f} км/ч; '
                f'{self.text_calories}: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    COEFF_TIME: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_hours: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration_hours
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2) * self.weight_kg
                           / self.M_IN_KM
                           * self.duration_hours * self.COEFF_TIME)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.coeff_calorie_1 * self.weight_kg
                           + (self.get_mean_speed() ** 2 // self.height_cm)
                           * self.coeff_calorie_2 * self.weight_kg)
                           * self.duration_hours * self.COEFF_TIME)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM
                        / self.duration_hours)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.get_mean_speed() + self.coeff_calorie_1)
                           * self.coeff_calorie_2 * self.weight_kg)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainin_types: Dict[str, type] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}
    if workout_type in trainin_types:
        training: Training = trainin_types[workout_type](*data)
        return training
    else:
        print('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
