"""Stworzyć funkcję, która przyjmie 3 argumenty typu int i sprawdzi czy suma
dwóch pierwszych liczb jest większa lub równa trzeciej, a następnie zwróci tę
informację jako typ logiczny bool"""


def check_sum(a: int, b: int, c: int) -> bool:
    return (a + b) >= c


if __name__ == "__main__":
    result = check_sum(5, 10, 17)
    print(result)
