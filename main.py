from abc import ABC, abstractmethod


class Storage(ABC):  # абстрактный класс
    @abstractmethod
    def __init__(self, items: dict, capacity: int):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, title: str, count: int) -> bool:
        """ добавление товаров """
        try:
            self.get_items()[title] += count
        except:
            self.get_items()[title] = count
        return True

    @abstractmethod
    def remove(self, title: str, count: int) -> bool:
        """ убавление товаров """
        try:
            self.get_items()[title] -= count
        except:
            return False
        if self.get_items()[title] == 0:  # если товара не осталось, удаляем из словаря
            self._items.pop(title)
        return True

    def get_free_space(self) -> int:
        """ вычисление свободного места """
        return self._capacity - sum(self._items.values())

    def get_items(self) -> dict:
        """ список товаров с количеством """
        return self._items

    def get_unique_items_count(self) -> int:
        """ ассортимент товаров """
        return len(self._items.keys())


class Store(Storage):
    # класс склад
    def __init__(self, items: dict, capacity=100):
        super().__init__(items, capacity)

    def __repr__(self) -> str:
        return "на склад"

    def add(self, title: str, count: int) -> bool:
        """ добавление товаров при наличии свободного места """
        if self.get_free_space() >= count: return super().add(title, count)
        return False

    def remove(self, title: str, count: int) -> bool:
        """ убавляем товар, если есть столько товара """
        try:
            self.get_items()[title]
        except:
            return False
        else:
            if self.get_items()[title] >= count: return super().remove(title, count)
        return False


class Shop(Storage):
    # класс магазин
    def __init__(self, items: dict, capacity=20):
        super().__init__(items, capacity)

    def __repr__(self) -> str:
        return "в магазин"

    def add(self, title: str, count: int) -> bool:
        """ добавление товаров при наличии свободного места и если разных товаров <5 """
        if self.get_unique_items_count() < 5 and self.get_free_space() >= count:
            return super().add(title, count)
        return False

    def remove(self, title: str, count: int) -> bool:
        try:
            self.get_items()[title]
        except:
            return False
        else:
            if self.get_items()[title] >= count: return super().remove(title, count)
        return False

class Request:  # класс перемещения товара
    def __init__(self, u_request: str):
        list_word = u_request.split()  # парсим входную строку
        self._from = list_word[4]
        self._to = list_word[6]
        self._amount = int(list_word[1])
        self._product = list_word[2]

    def __repr__(self) -> str:
        return f"Доставить {self._amount} {self._product} из {self._from} в {self._to}"

    def move_product(self, mag: Shop | Store, stor: Shop | Store) -> str:
        obj_1, obj_2 = stor, mag
        if self._from == "магазин" and self._to == "склад":
            obj_2, obj_1 = stor, mag  # меняем объекты местами при необходимости

        rezult = ""
        if obj_1.remove(self._product, self._amount):  # пробуем забрать товар
            rezult += f"Нужное количество есть {str(obj_1)}е\n"
            if obj_2.add(self._product, self._amount):  # пробуем довавить товар
                s1 = f"{self._amount} {self._product}"
                s2 = str(obj_1).replace('на', 'со').replace('в', 'из') + "а"
                s3 = str(obj_2)

                rezult += f"Курьер забрал {s1} {s2}\n"
                rezult += f"Курьер везет {s1} {s2} {s3}\n"
                rezult += f"Курьер доставил {s1} {s2} {s3}\n"
            else:
                obj_1.add(self._product, self._amount)  # возвращаем товар, если добавить не получится
                s1 = str(obj_2).capitalize()
                rezult += f"{s1}е недостаточно места, попробуйте что то другое\n"
        else:
            rezult += f"Не хватает {obj_1}е, попробуйте заказать меньше\n"
        return rezult


def main():
    store = Store({})
    shop = Shop({})
    store.add("колбаса", 10)
    store.add("хлеб", 10)
    store.add("сыр", 10)
    shop.add("колбаса", 3)
    shop.add("хлеб", 8)
    shop.add("сыр", 5)
    shop.add("мука", 1)
    # вывод исходного состояния
    print(f"на складе: {store.get_items()}\nв магазе: {shop.get_items()}")
    print("-" * 30)
    # ввод
    req1 = input("введите товар: ")
    req2 = input("введите количество: ")
    req3 = input("введите откуда забрать: ")
    req4 = input("введите куда доставить: ")
    per = Request(f"Доставить {req2} {req1} из {req3} в {req4}")
    print("\n" + str(per))
    print(per.move_product(shop, store))
    # вывод результата перемещения
    print(f"на складе: {store.get_items()}\nв магазе: {shop.get_items()}")


if __name__ == '__main__':
    main()
