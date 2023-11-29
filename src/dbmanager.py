import psycopg2


class DBManager:
    def __init__(self, params):
        """ Менеджер по управлению запросами к базе данных """
        self.__params = params

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """
        print('Вакансии по компаниям')
        try:
            with psycopg2.connect(**self.__params) as conn:
                with conn.cursor() as cur:
                    sql_request = """ select company_name, count(*) from vacancies inner join companies on vacancies.company_id = companies.company_id group by company_name; """
                    cur.execute(sql_request)
                    answer = cur.fetchall()
                    for item in answer:
                        print(f'Компания: {item[0]}, вакансия: {item[1]}')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию """
        print('Все вакансии')
        try:
            with psycopg2.connect(**self.__params) as conn:
                with conn.cursor() as cur:
                    sql_request = """ select company_name, vacancy_title, salary, currency, url from vacancies inner join companies on vacancies.company_id = companies.company_id order by company_name; """
                    cur.execute(sql_request)
                    answer = cur.fetchall()
                    for item in answer:
                        print(
                            f'Компания: {item[0]}, вакансий: {item[1]}, зарплата: {item[2]} {item[3]}, url: {item[4]}')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям """
        print('Средняя зарплата')
        try:
            with psycopg2.connect(**self.__params) as conn:
                with conn.cursor() as cur:
                    sql_request = """ select avg(salary), currency from vacancies group by currency; """
                    cur.execute(sql_request)
                    answer = cur.fetchall()
                    for item in answer:
                        print(f'Средняя зарплата: {item[0]} {item[1]}')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        print('Вакансии выше средней')
        try:
            with psycopg2.connect(**self.__params) as conn:
                with conn.cursor() as cur:
                    sql_request = """ select avg(salary), currency from vacancies group by currency; """
                    cur.execute(sql_request)
                    answer = cur.fetchall()
                    average = 0
                    currency = ''
                    for item in answer:
                        average = item[0]
                        currency = item[1]
                        print(f'Вакансии выше средней {average} по валюте {currency}')
                        sql_request = """ select company_name, vacancy_title, salary, currency, url from vacancies inner 
                                        join companies on vacancies.company_id = companies.company_id 
                                        where salary > %s and currency = %s order by company_name, salary desc; """
                        cur.execute(sql_request, (average, currency))
                        answer = cur.fetchall()
                        for item in answer:
                            print(f'Компания: {item[0]}, вакансия: {item[1]}, зарплата: {item[2]} {item[3]}, url: {item[4]}')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python """
        print(f'Вакансии с ключевым словом {keyword}')
        try:
            with psycopg2.connect(**self.__params) as conn:
                with conn.cursor() as cur:
                    sql_keyword = '%' + keyword + '%'
                    sql_request = """ select company_name, vacancy_title, salary, currency, 
                                        url from vacancies inner join companies on vacancies.company_id = companies.company_id 
                                        where vacancy_title like %s; """
                    cur.execute(sql_request, (sql_keyword,))
                    answer = cur.fetchall()
                    for item in answer:
                        print(
                            f'Компания: {item[0]}, вакансий: {item[1]}, зарплата: {item[2]} {item[3]}, url: {item[4]}')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
