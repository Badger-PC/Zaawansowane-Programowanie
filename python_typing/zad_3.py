'''Stworzyć funkcję, która będzie sprawdzała czy przekazana liczba w
parametrze jest parzysta i zwróci tą informację jako typ logiczny bool
( True / False ). Należy uruchomić funkcję, wynik wykonania zapisać do
zmiennej, a następnie wykorzystując warunek logiczny wyświetlić prawidłowy
tekst "Liczba parzysta" / "Liczba nieparzysta"'''
def is_even(number: int) -> bool:
 
    if number % 2 == 0:
        print("Liczba parzysta")
    else:
        print("Liczba nieparzysta")
    return 
if __name__ == '__main__':
    result = is_even(4)