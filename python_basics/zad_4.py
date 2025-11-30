
def filter_every_second_number(nums: list) -> list:
  
    return [nums[i] for i in range(len(nums)) if i % 2 == 0]

if __name__ == '__main__':
    print('Zadanie 1 D')
    print(filter_every_second_number([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]))
