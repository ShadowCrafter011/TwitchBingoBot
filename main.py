from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
from bingo import Bingo
import traceback


def main():
    load_dotenv()

    bingos = 0

    while True:
        bingo = Bingo(bingos)

        try:
            bingo.login()
            bingo.run()
        except KeyboardInterrupt:
            print(f"\nGot {bingo.bingos} bingo{"s" if bingo.bingos != 1 else ""}")
            break
        # Do nothing if tab crashes
        except WebDriverException:
            pass
        except:
            print(traceback.format_exc())
            pass
        finally:
            bingos = bingo.bingos
            bingo.quit()


if __name__ == "__main__":
    main()
