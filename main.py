import csv
import json

import matplotlib.pyplot as plt
from math import ceil


class Titanic:
    def __init__(self, path_name: str):
        self.path_name = path_name
        self._class_sex_data = {}
        self._sex_class_data = {}
        self.__get_parch_data_dict()

    def get_class(self) -> dict:
        return self._class_sex_data

    def get_sex(self) -> dict:
        return self._sex_class_data

    def _parse_sex_data(self, row: list) -> None:
        if not row[4] in self._class_sex_data:
            self._sex_class_data[row[4]] = {
                '1': 0,
                '2': 0,
                '3': 0,
            }
        self._sex_class_data[row[4]][row[2]] += 1

    def _parse_class_data(self, row: list) -> None:
        if not row[2] in self._class_sex_data:
            self._class_sex_data[row[2]] = {
                'female': 0,
                'male': 0
            }
        self._class_sex_data[row[2]][row[4]] += 1

    def __get_parch_data_dict(self) -> None:
        with open(self.path_name, 'r') as f:
            next(f)
            file = csv.reader(f, delimiter=',')
            for row in iter(file):
                self._parse_class_data(row)
                self._parse_sex_data(row)
            self._class_sex_data = dict(sorted(self._class_sex_data.items()))

    @staticmethod
    def draw_pie(data: dict) -> None:
        fig, axs = plt.subplots(1, 3, figsize=(9, 6))
        l1 = 0
        for key in data:
            axis = axs[l1]
            x = [data[key][x] for x in data[key]]
            label = [x for x in data[key]]
            axis.pie(x, labels=label, autopct='%1.1f%%')
            axis.set_title(f'Каюта класса {key}')
            l1 += 1
        fig.suptitle("Диаграмма соотношения мужчин и женщин в каютах разных классов")
        plt.show()


if __name__ == '__main__':
    path = "data/data.csv"
    titanic = Titanic(path)
    class_people = titanic.get_class()
    titanic.draw_pie(class_people)
    print(f'''
                            Таблица выживших
    ________________________________________
    |        | Класс 1 | Класс 2 | Класс 3 |
    |--------|---------|---------|---------|
    | Мужчин |{class_people['1']['male']:>6}{'|':>4}{class_people['2']['male']:>6}{'|':>4}{class_people['3']['male']:>6}{'|':>4}
    | Женщин |{class_people['1']['female']:>6}{'|':>4}{class_people['2']['female']:>6}{'|':>4}{class_people['3']['female']:>6}{'|':>4}
    |--------|---------|---------|---------|''')
