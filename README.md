## Гайд на репозиторий

### Начало работы

1. Необходимо установить Mamba. [Ссылка на гайд](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)

2. Если не хотите работать через *miniforge prompt*, то выполните там следующую команду:

        mamba init powershell
4. Необходимо для начала создать окружение:

        mamba create -f environment.yml
5. После обновления зависимостей в проекте нужно их подтягивать:

        mamba env update -f environment.yml

Всё, вы готовы к работе!

### Структура проекта

Проект пока что не имеет чёткой структуры. Сам проект - это python-модуль и весь код находится в *src/*

### Оформление кода

1. Вся работа оформляется в **отдельной ветке** и затем отправляется в **пулл реквест**

2. Важный аспект - это **наличие корректных тайпингов** (пока они в actions не настроены), **докстрингов** и так далее:

        def example(items: list[tuple[str, int]]) -> dict[str, int]:
            '''
            Transforms key-value list into a dict
            :param items: list of [key, value] pairs
            :returns: key-value dict 
            '''
            return {k: v for k, v in items}
3. Кавычки используем только **одинарные**, в качестве отступов используем **таб**
4. Стараемся валидировать входные данные с помощью assert'ов
