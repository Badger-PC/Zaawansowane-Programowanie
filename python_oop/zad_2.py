'''Stworzyć klasy reprezentujące: Library, Book, Employee, Student, Order.

Każda klasa ma mieć zaimplementowaną metodę __str__ , która będzie
opisywała obiekt oraz ewentualne obiekty znajdujące się w tym obiekcie
(np. obiekt Library w obiekcie Book).
Pola w klasie mają być zdefiniowane jako atrybuty ustawiane podczas
tworzenia instancji klasy za pośrednictwem konstruktora.
Stworzyć 2 biblioteki (2 instancje klasy), 5 książek, 3 pracowników, 3
studentów, oraz 2 zamówienia.
Wyświetlić oba zamówienia ( print )'''

class Library:
	def __init__(self, city, street, zip_code, open_hours:str, phone):
		self.city = city
		self.street = street
		self.zip_code = zip_code
		self.open_hours = open_hours
		self.phone = phone

	def __str__(self):
		return f"Biblioteka(Miasto={self.city}, ulica={self.street}, kod_pocztowy={self.zip_code}, godziny_otwarcia={self.open_hours}, telefon={self.phone})"


class Employee:
	def __init__(self, first_name, last_name, hire_date, birth_date, city, street, zip_code, phone):
		self.first_name = first_name
		self.last_name = last_name
		self.hire_date = hire_date
		self.birth_date = birth_date
		self.city = city
		self.street = street
		self.zip_code = zip_code
		self.phone = phone

	def __str__(self):
		return f"Pracownik(imie={self.first_name}, nazwisko={self.last_name}, data_zatrudnienia={self.hire_date}, data_urodzenia={self.birth_date}, miasto={self.city}, ulica={self.street}, kod_pocztowy={self.zip_code}, telefon={self.phone})"


class Book:
	def __init__(self, library, publication_date, author_name, author_surname, number_of_pages, title=None):
		self.library = library
		self.publication_date = publication_date
		self.author_name = author_name
		self.author_surname = author_surname
		self.number_of_pages = number_of_pages
		self.title = title

	def __str__(self):
		lib_str = str(self.library) if self.library is not None else 'None'
		title_part = f", tytuł={self.title}" if self.title else ""
		return f"Książka(tytuł={self.title or 'Nieznany/Księga Gada Jasnowidza'}{title_part}, data_wydania={self.publication_date}, autor={self.author_name} {self.author_surname}, liczba_stron={self.number_of_pages}, biblioteka={lib_str})"


class Order:
	def __init__(self, employee, student, books, order_date):
		self.employee = employee
		self.student = student
		self.books = list(books)
		self.order_date = order_date

	def __str__(self):
		emp_str = str(self.employee) if self.employee is not None else 'None'
		student_str = ''
		if isinstance(self.student, dict):
			parts = [f"{k}={v}" for k, v in self.student.items()]
			student_str = '{' + ', '.join(parts) + '}'
		else:
			student_str = str(self.student)
		books_str = '\n'.join([f"  - {str(b)}" for b in self.books])
		return f"Order(order_date={self.order_date}, employee={emp_str}, student={student_str}, books=[\n{books_str}\n])"


lib1 = Library('W*rszawa', 'Wiejska 40', '41-201', '9:00-17:00', '111-222-333')
lib2 = Library('Katowice', 'Bogudzicka 2', '48-501', '10:00-18:00', '222-111-111')

book1 = Book(lib1, '2001-05-20', 'Marek', 'Borczuk', 320, title='Pythony dla każdego')
book2 = Book(lib1, '1999-11-11', 'Maria', 'Borczuk', 210, title='Historia Polski od 1918 p..n.e. do dziś')
book3 = Book(lib2, '2015-07-07', 'Marcel', 'Borczuk', 150, title='Podstawy matematyki oraz fizyka kwantowa')
book4 = Book(lib2, '2020-02-02', 'Marcin', 'Borczuk', 480, title='Nowoczesne programowanie w Asemblerze')
book5 = Book(lib1, '2010-10-10', 'Macus', 'Borczuk', 95, title='Literatura piękna i brzydka')

emp1 = Employee('Cirilla', 'Środek', '2010-01-05', '1985-03-12', 'W*rszawa', 'Polna 3', '41-002', '600-700-800')
emp2 = Employee('Gniewomir', 'Dół', '2015-06-15', '1990-08-20', 'Katowice', 'Rolna 3', '42-002', '601-701-801')
emp3 = Employee('Celina', 'Góra', '2020-09-01', '1995-12-01', 'W*rszawa', 'Dworna 3', '43-003', '602-702-802')

student1 = {'first_name': 'Ewa', 'last_name': 'Adamska', 'birth_date': '0000-01-02'}
student2 = {'first_name': 'Adam', 'last_name': 'Boski', 'birth_date': '0000-01-01'}
student3 = {'first_name': 'Rafał', 'last_name': 'Wężowski', 'birth_date': '0001-09-01'}

order1 = Order(emp1, student1, [book1, book3], '2025-11-30')
order2 = Order(emp2, student2, [book2, book4, book5], '2025-11-29')

print(order1)
print(order2)
