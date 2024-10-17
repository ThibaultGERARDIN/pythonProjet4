"""Program launcher"""

from controllers.base import Controller


def main():

    controller = Controller()
    controller.display_main_menu()


if __name__ == "__main__":
    main()
