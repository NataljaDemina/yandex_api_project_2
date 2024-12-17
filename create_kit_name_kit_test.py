# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request

# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data

# Возвращаем ключ аутентификации
def get_user_token():
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(data.user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201

    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""
    
    return user_response.json()["authToken"]


# эта функция меняет значения в параметре name
def get_kit_body(name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.kit_body.copy()

    # изменение значения в поле name
    current_body["name"] = name
    # возвращается новый словарь с нужным значением firstName
    return current_body


# Возвращаем заголовок для создания набора 
def get_kit_header():
    header_body = data.headers.copy()
    token = get_user_token()
    print("User token:", token)
    header_body["Authorization"] = "Bearer " + token

    return header_body

# Функция для позитивной проверки
def create_kit_positive_assert(kit_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    create_kit_response = sender_stand_request.post_new_client_kit(get_kit_body(kit_name), get_kit_header())

    # Проверяется, что код ответа равен 201
    assert create_kit_response.status_code == 201

    # Проверяется, что в ответе есть верное имя набора
    assert create_kit_response.json()["name"] == kit_name

# Функция для негативной проверки создания набора
def create_kit_negative_assert(kit_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    create_kit_response = sender_stand_request.post_new_client_kit(get_kit_body(kit_name), get_kit_header())

    # Проверяется, что код ответа равен 400
    assert create_kit_response.status_code == 400

    # Проверка текста в теле ответа в атрибуте "message"
    assert create_kit_response.json()["message"] == "Не все необходимые параметры были переданы"

# Функция для негативной проверки создания набора (не передает имя набора)
def create_kit_noname_negative_assert():
    # В переменную user_body сохраняется обновлённое тело запроса
    create_kit_response = sender_stand_request.post_new_client_kit({}, get_kit_header())

    # Проверяется, что код ответа равен 400
    assert create_kit_response.status_code == 400

    # Проверка текста в теле ответа в атрибуте "message"
    assert create_kit_response.json()["message"] == "Не все необходимые параметры были переданы"

### ТЕСТЫ

# Тест 1. Допустимое количество символов в поле name(1)
def test_create_kit_1_letter_in_name_get_success_response():
    create_kit_positive_assert("a")    

# Тест 2. Допустимое количество символов (511)
def test_create_kit_511_letter_in_name_get_success_response():
    create_kit_positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Количество символов меньше допустимого (0)
def test_create_kit_0_letter_in_name_negative_response():
    create_kit_negative_assert("")

# Тест 4. Количество символов больше допустимого (512)
def test_create_kit_512_letter_in_name_negative_response():
    create_kit_negative_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Тест 5. Разрешены английские буквы
def test_create_kit_eng_letter_in_name_get_success_response():
    create_kit_positive_assert("QWErty") 

# Тест 6. Разрешены русские буквы
def test_create_kit_rus_letter_in_name_get_success_response():
    create_kit_positive_assert("Мария") 

# Тест 7. Разрешены спецсимволы
def test_create_kit_special_character_letter_in_name_get_success_response():
    create_kit_positive_assert("№%@")

# Тест 8. Разрешены пробелы
def test_create_kit_special_space_in_name_get_success_response():
    create_kit_positive_assert("Человек и КО ")

# Тест 9. Разрешеы цифры
def test_create_kit_numbers_in_name_get_success_response():
    create_kit_positive_assert("123 ")

# Тест 10. Параметр не передан в запросе
def test_Create_kit_noname_negaitve_response():
    create_kit_noname_negative_assert()

# Тест 11. Передан другой тип параметра (число)
def test_create_kit_numbers_letter_in_name_negative_response():
    create_kit_negative_assert(123)
    