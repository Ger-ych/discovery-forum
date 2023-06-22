<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h2 align="center">DiscoveryForum</h2>

  <p align="center">
    Онлайн-площадка.
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#описание">Описание</a>
    </li>
    <li>
      <a href="#разворачивание-проекта">Разворачивание проекта</a>
    </li>
    <li>
      <a href="#документация-к-rest-api">Документация к REST API</a>
    </li>
  </ol>
</details>


<!-- DESCRIPTION -->
## Описание

DiscoveryForum - это онлайн-площадка, где пользователи могут задавать вопросы по различным темам, а другие участники форума могут отвечать на эти вопросы, делиться своими знаниями и опытом, а также давать рекомендации и советы.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- DEPLOYMENT  -->
## Разворачивание проекта

TODO

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- REST API DOCUMENTATION -->
## Документация к REST API

Для того, чтобы обратиться к некоторым методам, вы должны быть авторизованы.

Для авторизации в заголовке Authorization необходимо передавать ваш AUTH TOKEN:

```Authorization: Token <AUTH TOKEN>```

Запрос может завершиться с ошибкой. Пример ответа с ошибкой:

```json
{
  "detail": "<Сообщение>"
}
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Регистрация

#### `POST /api/v1/auth/users/`

Создание новой учётной записи.

#### Запрос:
```json5
{
  "email": <Email> (str),
  "username": <Имя пользователя> (str),
  "password": <Пароль> (str)
}
```

#### Ответ:
```json5
201 Created

{
  "email": <Email> (str),
  "username": <Имя пользователя> (str),
  "id": <ID пользователя> (int)
}
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Вход

#### `POST /api/v1/auth/token/login/`

Получение токена авторизации (AUTH TOKEN).

#### Запрос:
```json5
{
  "username": <Имя пользователя> (str),
  "password": <Пароль> (str)
}
```

#### Ответ:
```json5
200 OK

{
  "auth_token": <Токен авторизации (AUTH TOKEN)> (str)
}
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Выход

#### `POST /api/v1/auth/token/logout/` `Требуется авторизация`

Удаление текущего токена авторизации (AUTH TOKEN).

#### Ответ:
```json5
204 No Content
```

<p align="right">(<a href="#top">back to top</a>)</p>
