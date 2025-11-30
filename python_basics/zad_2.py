
def multiply_by_two_for(nums: list) -> list:
  
    result = []
    for x in nums:
        result.append(x * 2)
    return result

def multiply_by_two_comp(nums: list) -> list:
  
    return [x * 2 for x in nums]

if __name__ == '__main__':
    print('Zadanie 1 B')
    print(multiply_by_two_for([1, 2, 3, 4, 5]))
    print('for loop version')
    print(multiply_by_two_comp([1, 2, 3, 4, 5]))
    print('lista składana version')