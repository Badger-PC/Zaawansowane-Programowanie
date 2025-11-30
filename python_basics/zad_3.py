
def filter_even_numbers(nums: list) -> list:
  
    return [x for x in nums if x % 2 == 0]

def filter_even_numbers_in_range(nums: list) -> list:
  
    result = []
    for x in range(len(nums)):
        if x % 2 == 0:
            result.append(x)
    return result

if __name__ == '__main__':
    print('Zadanie 1 C')
    print(filter_even_numbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print('in range version')
    print(filter_even_numbers_in_range([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    