import typebot
from threading import Thread

'''
Config description:
    webdriver: 'chrome' or 'firefox'
    run_headless: if true, will run headlessly (without opening a browser)
    should_login: if true, will use login_credentials to login
    login_credentials:
        username: your username to the site
        password: your password to the site
    wpm: words per minute you want the bot to type at (approx)
        - Note: if this is over 100 WPM and you have never reached that
          before, you may have to do a typing test with pictures
    start_delay: number of seconds to delay after race starts
    load_timeout: number of seconds to wait for webpage to load (internet speed)
    save_screenshot: if true, will save the end result screenshot to downloads
'''

# Modify the object below to configure the behaviour:
config = {
    'webdriver': 'firefox',
    'run_headless': False,
    'should_login': False,
    'login_credentials': {
        'username': 'your_username',
        'password': 'your_password'
    },
    'wpm': 150,
    'start_delay': 0,
    'load_timeout': 1,
    'save_screenshot': False
}

def main():
    bot = typebot.TypeBot(config)
    bot.run()


if __name__ == '__main__':
    main()
