from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
from bingo import Bingo
import traceback
import os


def main():
    load_dotenv()

    bingos = {}

    print("Available bingo channels are:")
    for key in os.environ.keys():
        if key.startswith("BINGO_URL"):
            print(key.replace("BINGO_URL_", "").lower().capitalize())
    
    channel = input("Which channel would you like to play bingo for? ")
    os.environ["BINGO_CHANNELS"] = channel.upper()

    while True:
        bingo = Bingo(bingos)

        try:
            bingo.login()
            bingo.run()
        except KeyboardInterrupt:
            print("\n")
            for channel, b in bingos.items():
                channel = channel.lower().capitalize()
                print(f"Got {b} bingo{"s" if b != 1 else ""} ({channel})")
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
