import plac
from selenium import webdriver
from src.udemy import Udemy
from src.errors import Error, LoginNotFound

import configparser
from config import UDEMY, COUPONS, Config

@plac.annotations(
    pages=plac.Annotation("Number of pages to scan", "option"),
    keywords=plac.Annotation("Path to the keywords file", "option"),
    driverpath=plac.Annotation("Path to the web driver", "option"),
    config=plac.Annotation("Path to the config file", "option")
)
def main(pages, keywords, driverpath, config=".config/config.ini"):
    try:
        options = Config(config, pages, keywords, driverpath)
    except configparser.Error:
        print("Impossible to parse the config file")
        exit(1)
    except KeyError:
        print("Invalid configuration file")
        exit(1)
    except ValueError:
        print("Configuration value given is invalid")
        exit(1)

    try:
        keys = list(options.keywords())
    except (IOError, FileNotFoundError):
        print("Impossible to open keywords file")
        exit(1)    

    code = 0 # Exit code of the App

    driver = webdriver.Firefox(executable_path=options.driver)
    driver.implicitly_wait(2)

    udemy = Udemy(driver, keys)
    try:
        udemy.login(UDEMY, options.user, options.password)
        udemy.extract(COUPONS, options.pages)
    except LoginNotFound:
        print("Error while communicating with the website DOM")
        code = 1
    except Error:
        print("Unknown custom error found while running the app")
        code = 1
    except:
        print("Unknown error found while running the app")
        code = 1
    finally:
        driver.close()

    exit(code)

def test_dummy():
    pass

if __name__ == "__main__":
    plac.call(main, version="0.2.0")
