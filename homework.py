class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
                   f'Дистанция: {"{:.3f}".format(self.distance)} км; '
                   f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
                   f'Потрачено ккал: {"{:.3f}".format(self.calories)}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    name = 'Тренировка'

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
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
        info_message = InfoMessage(self.name, self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    name = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        minutes = 60  # кол-во минут в часе, т.к. duration в часах
        calories = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * self.duration * minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    name = 'SportsWalking'

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
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 2
        coeff_calorie_5 = 0.029
        minutes = 60  # кол-во минут в часе, т.к. duration в часах
        calories = ((coeff_calorie_3 * self.weight
                    + (self.get_mean_speed() ** coeff_calorie_4 // self.height)
                    * coeff_calorie_5 * self.weight) * self.duration * minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    name = 'Swimming'

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
        speed = ((self.length_pool * self.count_pool / self.M_IN_KM)
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_6 = 1.1
        coeff_calorie_7 = 2
        calories = ((self.get_mean_speed() + coeff_calorie_6)
                    * coeff_calorie_7 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type == 'SWM':
        training_object = training_dict['SWM'](*data)
    if workout_type == 'RUN':
        action, duration, weight = data
        training_object = training_dict['RUN'](*data)
    if workout_type == 'WLK':
        action, duration, weight, height = data
        training_object = training_dict['WLK'](*data)
    return training_object


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
