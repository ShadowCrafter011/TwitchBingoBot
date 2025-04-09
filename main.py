from dotenv import load_dotenv
from bingo import Bingo
import traceback


def main():
    load_dotenv()

    bingo = Bingo()

    while True:
        try:
            bingo.login()
            bingo.run()
        except KeyboardInterrupt:
            break
        except:
            print(traceback.format_exc())

    bingo.quit()


if __name__ == "__main__":
    main()
