from src.api import HeadHunterAPI
from src.req_params import RequestEmployers, RequestVacanciesEmployer, RequestByDefault
import psycopg2
from src.env import EnvParameter
import os
from src.dbmanager import DBManager
import random


class UserInterface:
    def __init__(self, reload=''):
        self.__exit = False
        if reload == '0':
            print("Выполнение загрузки вакансий")
            cities, vacancies, employers = self._load_data()
            try:
                params = EnvParameter().db_key()
                with psycopg2.connect(**params) as conn:
                    with conn.cursor() as cur:

                        print('Создание таблиц...')
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        root_dir = os.path.split(current_dir)[0]
                        filepath = os.path.join(root_dir, os.path.normpath('data'), 'create_db.sql')
                        if os.path.isfile(filepath):
                            with open(filepath, 'r') as sql_file:
                                line = sql_file.read()
                                cur.execute(line)

                        print('Загрузка городов...')
                        sql_request = 'INSERT INTO cities VALUES ( %s, %s )'
                        for city in cities:
                            cur.execute(sql_request, (city['id'], city['name']))

                        print('Загрузка компаний...')
                        sql_request = 'INSERT INTO companies VALUES ( %s, %s, %s, %s )'
                        for employer in employers:
                            cur.execute(sql_request, (employer.employer_id,
                                                      employer.name, employer.get_area()['id'],
                                                      employer.get_open_vacancies()))

                        print('Загрузка вакансий...')
                        sql_request = 'INSERT INTO vacancies VALUES ( %s, %s, %s, %s, %s, %s, %s )'
                        for vacancy in vacancies:
                            cur.execute(sql_request, (vacancy.vacancy_id, vacancy.title,
                                                      vacancy.get_company()['id'], vacancy.get_area()['id'],
                                                      vacancy.salary.max_salary, vacancy.salary.currency, vacancy.link))

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    @property
    def exit(self):
        """ Флаг завершения работы """
        return self.__exit

    def execute(self):
        """ Выполнение основного алгоритма """
        print('Обработка базы...')
        dbmanager = DBManager(params=EnvParameter().db_key())
        dbmanager.get_companies_and_vacancies_count()
        dbmanager.get_all_vacancies()
        dbmanager.get_avg_salary()
        dbmanager.get_vacancies_with_higher_salary()
        keyword = input('Введите слово для поиска: ')
        if keyword == 'exit':
            self.__exit = True
        else:
            dbmanager.get_vacancies_with_keyword(keyword=keyword)

    def _load_data(self):
        all_vacancies = []
        cities = []
        platforma = HeadHunterAPI()
        request_default = RequestByDefault()
        request_for_employers = RequestEmployers(count=10)
        top_employers = platforma.get_employers(request_params=request_for_employers,
                                                request_employer=request_default)
        for employer in top_employers:

            area = employer.get_area()
            # пополняем базу городов
            if area not in cities:
                cities.append(area)

            open_count = employer.get_open_vacancies()
            pages = random.randint(1, 15)
            if open_count <= pages * 100:
                pages = open_count // 100
            for page in range(0, pages):
                request_for_vacancies = RequestVacanciesEmployer(employer_id=employer.employer_id, page=page)
                employers_vacancies = platforma.get_vacancies(request_params=request_for_vacancies)

                for vacancy in employers_vacancies:
                    # пополняем базу городов
                    area = vacancy.get_area()
                    if area not in cities:
                        cities.append(area)
                all_vacancies.extend(employers_vacancies)

        cities.sort(key=lambda x: x['id'])
        return cities, all_vacancies, top_employers
