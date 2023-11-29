class Employer:
    """ Класс содержаний информацию о работодателе """

    __Employers = []

    def __init__(self, employer_id, name, city, open):
        self.__employer_id = employer_id
        self.__name = name
        self.__city = city
        self.__open_vacancies = open

    @classmethod
    @property
    def employers(cls):
        """ Список вакансий """
        return cls.__Employers

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def name(self):
        return self.__name

    @property
    def city(self):
        return self.__city['name']

    def get_area(self):
        return self.__city

    def get_open_vacancies(self):
        return self.__open_vacancies
