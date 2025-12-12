class Property:
    def __init__(self, area, rooms, price, address):
        self.area = area
        self.rooms = int(rooms)
        self.price = price
        self.address = address


class House(Property):
    def __init__(self, area, rooms, price, address, plot):
        super().__init__(area, rooms, price, address)
        self.plot = int(plot)

    def __str__(self):
        return (
            f"Dom: {self.address}, powierzchnia: {self.area} m2, "
            f"pokoje: {self.rooms}, cena: {self.price}, działka: {self.plot} m2"
        )


class Flat(Property):
    def __init__(self, area, rooms, price, address, floor):
        super().__init__(area, rooms, price, address)
        self.floor = int(floor)

    def __str__(self):
        return (
            f"Mieszkanie: {self.address}, powierzchnia: {self.area} m2, "
            f"pokoje: {self.rooms}, cena: {self.price}, piętro: {self.floor}"
        )


if __name__ == "__main__":
    house = House(120, 5, 45000000, "ul. Złota 12, W*rszawa", 800)
    flat = Flat(60, 3, 320000, "ul. Bogudzicka 7, Katowice", 2)

    print(house)
    print(flat)
