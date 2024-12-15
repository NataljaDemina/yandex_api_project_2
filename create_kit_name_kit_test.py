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
    
    # print("User created. Token: ", user_response.json()["authToken"])
    return user_response.json()["authToken"]


# эта функция меняет значения в параметре name
def get_kit_body(name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.kit_body.copy()

    # изменение значения в поле name
    current_body["name"] = name
    # возвращается новый словарь с нужным значением firstName
    print("Kit body:", current_body)
    return current_body

# Возвращаем заголовок для создания набора 
def get_kit_header():
    header_body = data.headers.copy()
    token = get_user_token()
    print("User token:", token)
    header_body["Authorization"] = "Bearer {" + token + "}"

    print("Header body:", header_body)
    return header_body

# Функция для позитивной проверки
def create_kit_positive_assert(kit_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    create_kit_response = sender_stand_request.post_new_client_kit(get_kit_body("kit name"), get_kit_header())

    # Проверяется, что код ответа равен 201
    assert create_kit_response.status_code == 201

    # Проверяется, что в ответе есть верное имя набора
    assert create_kit_response.json()["name"] == kit_name

    # Проверяем, что такой набор доступен при запросе наборов пользователя
    

# Проверка функции создания набора
result = sender_stand_request.post_new_client_kit(get_kit_body("kit name"), get_kit_header())
print("Create kit status:", result.status_code)
print(result.json())