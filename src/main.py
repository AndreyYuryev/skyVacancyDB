from src.user_interface import UserInterface


def main():
    """ Обработка данных """
    interface = UserInterface()
    while not interface.exit:
        interface.execute()


if __name__ == '__main__':
    main()
