from src.user_interface import UserInterface


def main():
    """ Обработка данных """
    interface = UserInterface(reload=input('Для перезаписи таблиц БД введите 0: '))
    while not interface.exit:
        interface.execute()


if __name__ == '__main__':
    main()
