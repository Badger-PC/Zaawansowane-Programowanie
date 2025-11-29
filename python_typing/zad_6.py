'''Stworzyć funkcję, która przyjmuje 2 argumenty typu list i zwraca wynik typu
list . Funkcja ma za zadanie złączyć przekazane listy w jedną, usunąć
duplikaty, każdy element podnieść do potęgi 3 stopnia, a następnie zwrócić
powstałą listę.'''

def process_lists(list1: list, list2: list) -> list:
    combined = list1 + list2
    unique_elements = set(combined)
    processed = [x ** 3 for x in unique_elements]
    return processed
if __name__ == '__main__':
    lista_a = [1, 2, 3, 4, 5]
    lista_b = [4, 5, 6, 7, 8]
    wynik = process_lists(lista_a, lista_b)
    print(wynik)