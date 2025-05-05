from dotenv import load_dotenv
from bingo import Bingo
import traceback


def main():
    load_dotenv()

    while True:
        bingo = Bingo()

        try:
            bingo.login()
            bingo.run()
        except KeyboardInterrupt:
            print(f"\nGot {bingo.bingos} bingo{"s" if bingo.bingos != 1 else ""}")
            break
        except:
            print(traceback.format_exc())
        finally:
            bingo.quit()


if __name__ == "__main__":
    main()
