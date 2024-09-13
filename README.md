# yd_files

Yandex Disk files loader

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Описание проекта

Цель: просмотр и загрузка файлов по публичной ссылке Yandex Disk.

Реализация:

- Django 5.0.9, PostgreSQL 16, пока synchronous
- Форма ввода публичной ссылки
- сохранение файловой структуры Yandex Disk
- окно просмотра файлов с чекбоксами для выбора нескольких файлов
- загрузка выбранных файлов в zip формате
- просмотр содержимого вложенных папок на любую глубину
- детальный просмотр файла (превью, иконки, фото ...)
- база данных сохраняет сессии просмотров (публичные ссылки и просмотренные файлы)
- автоматическое обновление устаревших загрузочных ссылок
- документирование кода

Скриншоты:

[<img src="docs/images/img_01.png" width="500"/>]()
[<img src="docs/images/img_02.png" width="500"/>]()
[<img src="docs/images/img_03.png" width="500"/>]()
[<img src="docs/images/img_04.png" width="500"/>]()
[<img src="docs/images/img_05.png" width="500"/>]()
[<img src="docs/images/img_06.png" width="500"/>]()
[<img src="docs/images/img_10.png" width="500"/>]()
[<img src="docs/images/img_07.png" width="500"/>]()
[<img src="docs/images/img_08.png" width="300"/>]()
[<img src="docs/images/img_09.png" width="300"/>]()

TODO:

- Просмотр вложенных папок организовать по аналогии с видом главной страницы.

(папки кликабельны, файлы загружаются по чекбоксам, на экране копия файловой структуры Yandex Disk)
- добавить сортировку выводимых на экран фалов по их типу
- Вывести историю просмотров
- Вывести кнопку автоматического обновления устаревших ссылок, или нечто иное.
- многопоточная загрузка
- внешний вид (настроить шаблоны), тесты

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy yd_files

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
