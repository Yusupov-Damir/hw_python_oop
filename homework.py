from dataclasses import dataclass


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.

    Args:
            duration: часы
            distance: км
            speed: км/ч
            calories: Ккал
    """

    training_type: float
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """
        Возвращает информацию о тренировке
        строкой.
        """
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """
    Базовый класс тренировки.

    Const:
        LEN_STEP: метры
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Расчёт дистанции, которую
        пользователь преодолел за тренировку (км).
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Расчёт средней скорости
        движения во время тренировки (км/ч).
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """
        Расчёт количества калорий,
        израсходованных за тренировку (Ккал).
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Создание объекта сообщения
        о результатах тренировки.
        """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """
    Тренировка: бег.
    """

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """
        (Ккал)
        """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    """

    A = 0.035
    B = 0.029
    KMH_TO_MS = 0.278
    SM_TO_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        (Ккал)

        Args:
            mean_speed_in_ms - перевод в м/с
            hieght_in_m - перевод в метры
        """
        mean_speed_in_ms = self.get_mean_speed() * self.KMH_TO_MS
        hieght_in_m = self.height / self.SM_TO_M
        return ((self.A * self.weight
                + (mean_speed_in_ms**2 / hieght_in_m)
                * self.B * self.weight) * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """
    Тренировка: плавание.
    """

    LEN_STEP = 1.38
    C = 1.1
    D = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """
        (Ккал)
        """
        return ((self.get_mean_speed() + self.C)
                * self.D * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        """
        (км/ч)
        """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """
    Прочитать данные полученные от датчиков.
    """
    read_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in read_dict:
        return read_dict[workout_type](*data)
    else:
        raise ValueError(f'Неизвестный тип тренировки {workout_type}')


def main(training: Training) -> None:
    """
    Главная функция.
    """
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
