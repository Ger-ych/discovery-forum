<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">DiscoveryForum</h3>

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

Запрос:
```json
{
  "email": "<Email>",
  "username": "<Имя пользователя>",
  "password": "<Пароль>"
}
```

Ответ:
```json
{
  "email": "<Email>",
  "username": "<Имя пользователя>",
  "id": "<ID пользователя>"
}
```

<p align="right">(<a href="#top">back to top</a>)</p>
