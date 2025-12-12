"""Stworzyć klasę Student , która posiada 2 parametry (name i marks) oraz jedną
metodę is_passed, która zwraca wartość logiczną, pozytywną gdy średnia
ocen jest > 50 w przeciwnym przypadku negatywną. Następnie należy
stworzyć 2 przykładowe obiekty klasy, tak aby dla pierwszego obiektu metoda
zwracała true , a dla drugiego false .
"""


class Student:
    def __init__(self, name: str, marks: list[float]):
        self.name: str = name
        self.marks: list[float] = [float(m) for m in marks]

    def average(self) -> float:
        if not self.marks:
            return 0.0
        return sum(self.marks) / len(self.marks)

    def is_passed(self) -> bool:
        return self.average() > 50


if __name__ == "__main__":
    student_pass = Student("Mariusz", [60, 70, 40])
    student_fail = Student("Marek", [40, 50])

    print(
        f"{student_pass.name} średnia = {student_pass.average():.2f}, zdane? {student_pass.is_passed()}"
    )
    print(
        f"{student_fail.name} średnia = {student_fail.average():.2f}, passed? {student_fail.is_passed()}"
    )
