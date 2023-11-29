from abc import ABC, abstractmethod
from src.env import EnvParameter
from src.req_params import RequestParameter
from src.vacancy import Vacancy, Salary
from src.employer import Employer
import requests


class API(ABC):
    """ Класс для описания абстрактных методов API """

    def __init__(self, test_mode=False):
        """ Инициализировать атрибуты """
        self.__test_mode = test_mode

    @property
    def test_mode(self):
        """ Флаг тестового режима """
        return self.__test_mode

    def _get_response_json(self, url=str(), params=dict(), headers=dict()):
        """ Получить ответ на запрос и распарсить JSON """
        rsp = requests.get(url=url, params=params, headers=headers)
        rsp_json = rsp.json()
        return rsp_json

    @abstractmethod
    def _get_api_key(self):
        """ Получить ключ из переменных окружения """
        pass

    @abstractmethod
    def _create_headers(self):
        """ Создать словарь с заголовком запроса """
        pass

    @abstractmethod
    def _create_params(self, request_params: RequestParameter):
        """ Создать словарь с параметрами запроса """
        pass

    @abstractmethod
    def get_vacancies(self, request_params: RequestParameter):
        """ Получить словарь с вакансиями """
        pass

    @abstractmethod
    def get_employers(self, request_params: RequestParameter, request_employer: RequestParameter):
        """ Получить словарь с работодателями """
        pass


class SuperJobAPI(API):
    """ API для работы с вакансиями от superjob.ru """

    def __init__(self, test_mode=False):
        """ Инициализировать атрибуты """
        super().__init__(test_mode)
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__headers = self._create_headers()

    def _get_api_key(self):
        """ Получить api key для объекта с конструктором """
        if super().test_mode:
            return EnvParameter().api_key('TEST_SUPERJOB_API_KEY')
        else:
            return EnvParameter().api_key('SUPERJOB_API_KEY')

    def _create_headers(self):
        return {"X-Api-App-Id": self._get_api_key()}

    def _create_params(self, request_params: RequestParameter):
        params = request_params.params(api_sj=True)
        return params

    def get_vacancies(self, request_params: RequestParameter):
        vacancies = self._get_response_json(url=self.__url, headers=self.__headers,
                                            params=self._create_params(request_params=request_params))
        # print(f'\n----- SuperJob-----')
        sj_vacancies = []
        for vacancy in vacancies['objects']:
            # название вакансии
            title = vacancy.get('profession', 'Не указано')
            # ссылка на вакансию
            link = vacancy.get('link', 'Не указано')
            # город
            try:
                city = vacancy['town']['title']
            except KeyError:
                city = 'Не указано'
            # зарплата
            salary = Salary(salary_from=vacancy.get('payment_from', 0), salary_to=vacancy.get('payment_to', 0),
                            agreement=vacancy.get('agreement', False))
            # наименование компании работодателя
            company = vacancy.get('firm_name', 'Не указано')
            # описание вакансии
            description = 'Не указано'
            try:
                # description = vacancy['work']
                description = vacancy['vacancyRichText']
            except KeyError:
                pass
            vc = Vacancy(title=title, salary=salary, city=city, link=link, company=company, description=description,
                         platform='SJ')
            sj_vacancies.append(vc)
        return sj_vacancies

    def get_employers(self, request_params: RequestParameter, request_employer: RequestParameter):
        pass


class HeadHunterAPI(API):
    """ API для работы с вакансиями от headhunter.ru """

    def __init__(self, test_mode=False):
        """ Инициализировать атрибуты """
        super().__init__(test_mode)
        self.__url_vacancies = 'https://api.hh.ru/vacancies'
        self.__url_employers = 'https://api.hh.ru/employers'
        self.__headers = self._create_headers()

    def _get_api_key(self):
        """ Получить api key для объекта без конструктора """
        if super().test_mode:
            return EnvParameter().api_key('TEST_HEADHUNTER_API_KEY')
        else:
            return EnvParameter().api_key('HEADHUNTER_API_KEY')

    def _create_headers(self):
        return {}

    def _create_params(self, request_params: RequestParameter):
        params = request_params.params(api_hh=True)
        return params

    def get_vacancies(self, request_params: RequestParameter):
        vacancies = self._get_response_json(url=self.__url_vacancies, headers=self.__headers,
                                            params=self._create_params(request_params=request_params))
        # print(f'\n-----HeadHunter-----')
        hh_vacancies = []
        for vacancy in vacancies['items']:
            vacancy_id = vacancy['id']
            # название вакансии
            title = vacancy.get('name', 'Не указано')
            # ссылка на вакансию
            link = vacancy.get('alternate_url', 'Не указано')
            # город
            try:
                city = dict(id=vacancy['area']['id'], name=vacancy['area']['name'])
            except KeyError:
                city = {}

            # зарплата
            salary_object = vacancy.get('salary', None)
            if salary_object is None:
                salary = Salary(agreement=True)
            else:
                salary_from = salary_object.get('from', 0)
                currency = salary_object.get('currency', 'RUR')
                if salary_from is None:
                    salary_from = 0
                salary_to = salary_object.get('to', 0)
                if salary_to is None:
                    salary_to = 0
                if salary_from == salary_to and salary_from == 0:
                    salary = Salary(agreement=True)
                else:
                    salary = Salary(salary_from=salary_from, salary_to=salary_to, currency=currency)
            # наименование компании работодателя
            company = 'Не указано'
            try:
                company = dict(id=vacancy['employer']['id'], name=vacancy['employer']['name'])
            except KeyError:
                company = {}
            # описание вакансии
            description = 'Не указано'
            try:
                snippet = vacancy['snippet']
                description = snippet['requirement']
            except KeyError:
                pass

            vc = Vacancy(title=title, salary=salary, city=city, link=link, company=company, description=description,
                         platform='HH', vacancy_id=vacancy_id)
            hh_vacancies.append(vc)

        return hh_vacancies

    def get_employers(self, request_params: RequestParameter, request_employer: RequestParameter):
        hh_employers = []
        employers = self._get_response_json(url=self.__url_employers, headers=self.__headers,
                                            params=self._create_params(request_params=request_params))
        for item in employers['items']:
            employer_id = item['id']
            employer_url = '/'.join([self.__url_employers, employer_id])
            employer_info = self._get_response_json(url=employer_url, headers=self.__headers,
                                                    params=self._create_params(request_params=request_employer))
            employer = Employer(employer_id=employer_info['id'], name=employer_info['name'],
                                city=dict(id=employer_info['area']['id'], name=employer_info['area']['name']),
                                open=employer_info['open_vacancies'])
            hh_employers.append(employer)
        return hh_employers
