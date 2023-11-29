from abc import ABC, abstractmethod


class SearchParameter:
    """ Параметры поиска """

    def __init__(self, title: bool = False, company: bool = False, full: bool = True, keywords: list = [],
                 and_parameter: bool = False):
        self.__title = title
        self.__company = company
        self.__full = full
        self.__keywords = keywords
        self.__and_parameter = and_parameter

    def get_sj_params(self):
        """ Получить параметры для запроса SJ """
        params = dict()
        # формирование запроса
        # поиск везде по ключевым словам
        if self.__full:
            params['keyword'] = ' '.join(self.__keywords)
        else:
            pass
        return params

    def get_hh_params(self):
        """ Получить парамтеры для запроса HH """
        params = dict()
        # формирование запроса
        # поиск везде по ключевым словам
        if self.__full:
            params['text'] = ' '.join(self.__keywords)
        else:
            pass
        return params


class RequestParameter(ABC):
    """ Класс для описания абстрактных методов Request """

    def __init__(self, count=100, page=0, archive=False):
        self.__count = count
        self.__page = page
        self.__archive = archive

    @property
    def count(self):
        """ Количество на одной странице """
        return self.__count

    @property
    def page(self):
        """ Количество страниц """
        return self.__page

    @property
    def archive(self):
        """ Смотреть архив """
        return self.__archive

    @abstractmethod
    def params(self):
        """ Заполнение параметрами """


class RequestSearch(RequestParameter):
    """ Параметры поиска вакансии """

    def __init__(self, count=100, page=0, archive=False, search=SearchParameter(title=False, company=False)):
        super().__init__(count=count, page=page, archive=archive)
        self.__search = search

    @property
    def search(self):
        """ Список ключевых слов """
        return self.__search

    def params(self, api_hh: bool = False, api_sj: bool = False):
        """ Формирование параметров для запроса """
        params = dict()
        if api_hh:
            for key, value in self.search.get_hh_params().items():
                # формирование запроса
                # поиск везде по ключевым словам
                params[key] = value
        elif api_sj:
            for key, value in self.search.get_sj_params().items():
                # формирование запроса
                # поиск везде по ключевым словам
                params[key] = value
        params['count'] = self.count
        params['page'] = self.page
        params['archive'] = self.archive
        return params


class RequestEmployers(RequestParameter):
    def __init__(self, count=10, page=0, archive=False, sort_by='by_vacancies_open'):
        super().__init__(count=count, page=page, archive=archive)
        self.__sort_by = sort_by

    def params(self, api_hh: bool = False, api_sj: bool = False):
        """ Формирование параметров для запроса """
        params = dict()
        params['per_page'] = self.count
        params['page'] = self.page
        params['archive'] = self.archive
        if api_hh:
            params['sort_by'] = self.__sort_by
        return params


class RequestVacanciesEmployer(RequestParameter):
    def __init__(self, employer_id, count=100, page=0, archive=False, ):
        super().__init__(count=count, page=page, archive=archive)
        self.__employer_id = employer_id

    def params(self, api_hh: bool = False, api_sj: bool = False):
        """ Формирование параметров для запроса """
        params = dict()
        params['per_page'] = self.count
        params['page'] = self.page
        params['archive'] = self.archive
        if api_hh:
            params['employer_id'] = self.__employer_id
        return params


class RequestByDefault(RequestParameter):
    def __init__(self, count=100, page=0, archive=False, ):
        super().__init__(count=count, page=page, archive=archive)

    def params(self, api_hh: bool = False, api_sj: bool = False):
        """ Формирование параметров для запроса """
        params = dict()
        params['per_page'] = self.count
        params['page'] = self.page
        params['archive'] = self.archive
        return params
