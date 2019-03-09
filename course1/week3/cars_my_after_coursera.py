#
#
#
#

import os
import csv
import sys


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    # def __str__(self):
    #     return self.car_type + "_" + self.photo_file_name
    #
    # def __repr__(self):
    #     return self.car_type + "_" + self.photo_file_name

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]


class Car(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            whl = [float(size.strip()) for size in body_whl.split('x')]
        except ValueError:
            whl = [0., 0., 0.]
        self.body_width = whl[0]
        self.body_height = whl[1]
        self.body_length = whl[2]

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) != 7:
                continue
            if row[0] == "car":
                car = Car(row[0], row[1], row[3], row[5], row[2])
            if row[0] == "truck":
                car = Truck(row[0], row[1], row[3], row[5], row[4])
            if row[0] == "spec_machine":
                car = SpecMachine(row[0], row[1], row[3], row[5], row[6])
            car_list.append(car)
    return car_list


if __name__ == '__main__':
    print(get_car_list(sys.argv[1]))
