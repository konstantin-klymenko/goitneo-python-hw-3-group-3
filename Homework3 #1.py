import datetime #Howmework3

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if len(value) < 1:
            raise ValueError("Name can't be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

#Howmework3
class Birthday(Field):
    def __init__(self, value=None):
        if value:
            # Перевірте правильність формату дати народження
            try:
                datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None #Howmework3

    def add_phone(self, phone):
        try:
            phone = Phone(phone)
            self.phones.append(phone)
        except ValueError as e:
            print(e)

    #Howmework3
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "N/A" #Howmework3
        return f"Contact name: {self.name}, phones: {phone_str}, birthday: {birthday_str}" #Howmework3

#Howmework3
class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    #Howmework3
    def get_birthdays_per_week(self, users):
    # Створюємо словник для збереження іменнинників по днях тижня
        birthday_dict = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": []
        }
        
        # Отримуємо поточну дату
        today = datetime.today().date()
        
        # Перебираємо користувачів і аналізуємо їх дати народження
        for user in users:
            name = user["name"]
            birthday = user["birthday"].date()
            
            # Перевіряємо, чи вже минув день народження цього року
            if birthday < today:
                # Якщо так, розглядаємо дату на наступний рік
                birthday = birthday.replace(year=today.year + 1)
            
            # Обчислюємо різницю між днем народження і поточним днем
            delta_days = (birthday - today).days
            
            # Визначаємо день тижня для дня народження
            birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")
            
            # Перевіряємо, чи день народження припадає на вихідний
            if birthday_weekday in ["Saturday", "Sunday"]:
                # Якщо так, переміщаємо вітання на понеділок
                birthday_weekday = "Monday"
            
            # Додаємо ім'я до відповідного дня тижня в словнику
            birthday_dict[birthday_weekday].append(name)
        
        # Виводимо результат
        for day, names in birthday_dict.items():
            if names:
                print(f"{day}: {', '.join(names)}")

#Howmework3
def handle_add_birthday(book, args):
    if len(args) != 2:
        print("Usage: add-birthday [ім'я] [дата народження]")
        return
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
    else:
        print(f"Контакт з ім'ям {name} не знайдений")

#Howmework3
def handle_show_birthday(book, args):
    if len(args) != 1:
        print("Usage: show-birthday [ім'я]")
        return
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        print(f"День народження для {name}: {record.birthday.value}")
    elif record:
        print(f"Контакт {name} не має вказаного дня народження")
    else:
        print(f"Контакт з ім'ям {name} не знайдений")

#Howmework3
def handle_birthdays(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        print("Контакти для привітання на наступному тижні:")
        for record in birthdays:
            print(f"{record.name.value} ({record.birthday.value})")
    else:
        print("Немає контактів для привітання на наступному тижні")

def handle_show_all(book):
    for record in book.data.values():
        print(record)

def handle_add(book, args):
    if len(args) != 2:
        print("Usage: add [ім'я] [номер телефону]")
        return
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

def handle_all(book):
    for record in book.data.values():
        print(record)

# Функція для обробки команд користувача
def process_command(book, command):
    parts = command.split()
    if not parts:
        return

    if parts[0] == "add-birthday":
        handle_add_birthday(book, parts[1:])
    elif parts[0] == "show-birthday":
        handle_show_birthday(book, parts[1:])
    elif parts[0] == "birthdays":
        handle_birthdays(book)
    elif parts[0] == "all":  # Додайте обробник для команди "all"
        handle_all(book)
    elif parts[0] == "add":
        handle_add(book, parts[1:])
    else:
        # Інші обробники команд (add, change, phone, close, тощо)
        pass

# Створення нової адресної книги
book = AddressBook()

while True:
    command = input("Введіть команду: ")
    if command.lower() in ("close", "exit"):
        break
    process_command(book, command)