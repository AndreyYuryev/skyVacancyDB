''' Тесты для классов API с помощью pytest'''
import pytest
from src.vacancy import Vacancy, Salary


def test_salary():
    salary1 = Salary(salary_from=10000, salary_to=20000)
    salary2 = Salary(salary_from=15000, salary_to=20000, agreement=False)
    salary3 = Salary(agreement=True)
    salary4 = Salary(salary_from=25000, salary_to=30000)
    salary5 = Salary(agreement=True)
    salary6 = Salary()
    assert salary1.is_agreement() is False
    assert salary3.is_agreement()
    assert salary1 == salary2
    assert salary2 < salary4
    assert salary4 > salary1
    assert salary3 == salary5
    assert salary1 != salary3
    assert salary6.is_agreement() is True


def test_vacancy():
    Vacancy.vacancies.clear()
    salary = Salary(agreement=True)
    vacancy1 = Vacancy(title='vacancy 1', link='https:/testvacancy1.ru', salary=salary)
    vacancy2 = Vacancy(title='vacancy 2', city={'id':1, 'name': 'Moscow'}, salary=salary)
    vacancy3 = Vacancy(title='vacancy 3', company={'id': 1, 'name': 'Google'}, salary=salary)
    vacancy4 = Vacancy(title='vacancy 4', description='Description4', salary=salary)
    assert len(Vacancy.vacancies) == 4
    assert vacancy1.title == 'vacancy 1'
    assert vacancy2.title == 'vacancy 2'
    assert vacancy1.salary == salary
    assert vacancy1.link == 'https:/testvacancy1.ru'
    assert vacancy1.city == ''
    assert vacancy2.city == 'Moscow'
    assert vacancy3.company == 'Google'
    assert vacancy4.description == 'Description4'


def test_vacancy_salary():
    salary1 = Salary(salary_from=10000, salary_to=20000)
    salary2 = Salary(salary_from=15000, salary_to=25000)
    salary3 = Salary(agreement=True)
    vacancy1 = Vacancy(title='vacancy 1', salary=salary1)
    vacancy2 = Vacancy(title='vacancy 2', salary=salary2)
    vacancy3 = Vacancy(title='vacancy 3', salary=salary1)
    vacancy4 = Vacancy(title='vacancy 4', salary=salary3)
    vacancy5 = Vacancy(title='vacancy 5', salary=salary3)
    assert vacancy1 == vacancy3
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy3
    assert vacancy4 == vacancy5


# def test_vacancy_json():
#     salary1 = Salary(salary_from=15000, salary_to=25000)
#     salary2 = Salary(agreement=True)
#     vacancy1 = Vacancy(title='vacancy 1', company='company1', salary=salary1, platform='SJ')
#     vacancy2 = Vacancy(title='vacancy 2', link='test2.ru', salary=salary2, platform='HH')
#     assert vacancy1.get_json_data() == {'city': '', 'company': 'company1', 'description': '', 'link': '',
#                                         'salary': 25000, 'title': 'vacancy 1', 'platform': 'SJ'}
#     assert vacancy2.get_json_data() == {'city': '', 'company': '', 'description': '', 'link': 'test2.ru', 'salary': 0,
#                                         'salary_agreement': True, 'title': 'vacancy 2', 'platform': 'HH'}
