'''Stworzyć funkcję, która przyjmie 2 argumenty. Pierwszy typu list , a drugi
typu int . Funkcja ma sprawdzić (zwracając typ logiczny bool ), czy lista z
parametru pierwszego zawiera taką wartość jaką przekazano w parametrze
drugim.'''

def contains_value(values: list, value: int) -> bool:
    return value in values
if __name__ == '__main__':
    sample_list = [1, 2, 3, 4, 5]
    sample_value = 3
    result = contains_value(sample_list, sample_value)
    print(f"Czy lista {sample_list} zawiera wartość {sample_value}? {result}")