# skyVacancyDB

## Поиск вакансий на платформе HeadHunter с использованием PostgreSQL

Программа предназначена для вывода информации из базы данных по найденным вакансиям.
Поиск вакансий осуществляется в несколько этапов:
- Формирование базы вакансий на основе запросов
> Для формирования запросов используется модифицированный API проекта `skyVacancy`
 
- Работа с вакансиями из базы данных
> Для заполнения базы данных необходимо сохранить полученные данные в JSON-файлы

Для перезаписи базы необходимо вначале ввести 0.

При поиске вакансий сначала запрашивается топ-10 работодателей по количеству открытых вакансий.
Затем по каждому запрашивается до 1400 вакансий случайным образом.
Далее формируется список вакансий, работодателей и городов.
Запускается SQL скрипт создания таблиц для хранения данных:
> - CITIES
> - COMPANIES
> - VACANCIES

Затем запускается режим выполнения методов класса `DBManager`.
Для поиска по шаблону в названии вакансии нужно ввести ключевое слово,
для завершения выполнения программы нужно ввести `exit`. 