from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {}; Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60  # кол-во минут в часе, т.к. duration в часах

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('В родительском классе Training данный метод'
                                  'не определен и не выполняется')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__, self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUNNING_1: int = 18
    COEFF_CALORIE_RUNNING_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_RUNNING_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUNNING_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WALKING_1: float = 0.035
    COEFF_CALORIE_WALKING_2: int = 2
    COEFF_CALORIE_WALKING_3: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.name = 'SportsWalking'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_WALKING_1
                * self.weight
                + (self.get_mean_speed() ** self.COEFF_CALORIE_WALKING_2
                 // self.height)
                * self.COEFF_CALORIE_WALKING_3
                * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWIMMING_1: float = 1.1
    COEFF_CALORIE_SWIMMING_2: int = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return ((self.length_pool * self.count_pool / self.M_IN_KM)
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWIMMING_1)
                * self.COEFF_CALORIE_SWIMMING_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_dict.get(workout_type)(*data)


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
