from selenium import webdriver
from datetime import datetime
import time

# A TypeBot for play.typeracer.com
# To customize configurations: modify config in main.py
class TypeBot:
    def __init__(self, config):
        self.config = config
        self.driver = self.setup_driver(config)
        self.url = 'http://play.typeracer.com/'

    # Set up the web driver and return it
    def setup_driver(self, config):
        d = config['webdriver']
        run_headless = config['run_headless']
        if d == 'firefox':
            options = webdriver.firefox.options.Options()
            if run_headless:
                options.add_argument('--headless')
            return webdriver.Firefox(options=options)
        else:
            # Chrome as webdriver
            options = webdriver.chrome.options.Options()
            if run_headless:
                options.add_argument('--headless')
            return webdriver.Chrome(options=options)

    # Run the bot
    def run(self):
        self.driver.get(self.url)
        self.load_timeout()

        if self.config['should_login']:
            self.login(self.config['login_credentials'])
            print("Logged in as " + self.config['login_credentials']['username'])

        self.enter_race()
        self.load_timeout()

        text = self.get_text()
        print("Text to type: " + text)
        self.wait_for_start()

        print("Race starting.")
        time.sleep(self.config['start_delay'])
        self.type(text)
        print("Race ended.")
        self.load_timeout()
        if self.config['save_screenshot']:
            self.save_ss()
            self.driver.quit()

    # Sleep for the webpage to load
    def load_timeout(self):
        time.sleep(self.config['load_timeout'])

    # Save a screenshot at downloads
    def save_ss(self):
        path = datetime.now().strftime('downloads/SS%Y%m%d:%H%M%S.png')
        self.driver.save_screenshot(path)
        print("Screenshot saved at " + path)

    # Type a string, character by character, in text input
    def type(self, text):
        text_input = self.driver.find_element_by_class_name('txtInput')
        char_delay = self.char_delay(self.config['wpm'])
        for char in text:
            text_input.send_keys(char)
            time.sleep(char_delay)

    # Calculate the delay necessary for between each character given WPM
    def char_delay(self, wpm):
        # Accounts for the delay causedby key, sleep, etc
        adj_wpm = wpm + (0.09*wpm)**1.4
        return 60 / (adj_wpm * 5)

    # Wait until the race starts (when text input is not disabled)
    def wait_for_start(self):
        text_input = self.driver.find_element_by_class_name('txtInput')
        started = False
        while not started:
            time.sleep(0.1)
            if not text_input.get_attribute('disabled'):
                started = True

    # Enter the race
    def enter_race(self):
        self.driver.find_element_by_partial_link_text('Enter a typing race').click()

    # Fetch and parse the text elements into the text to be typed
    def get_text(self):
        elems = self.driver.find_elements_by_css_selector('span[unselectable="on"]')
        # parse text
        if len(elems) == 1:
            return elems[0].text
        if len(elems) > 2:
            if elems[0].get_attribute('class').split(' ')[0] == elems[1].get_attribute('class'):
                return elems[0].text + elems[1].text + ' ' + elems[2].text
        text = ''
        # default method when not matching any special cases
        for i in range(len(elems)):
            if i == len(elems)-1:
                text += ' '  # before the last elem, there is a space in between
            text += elems[i].text
        return text

    # Login, if given the credentials
    def login(self, credentials):
        if credentials:
            self.driver.find_element_by_link_text('Sign In').click()
            self.driver.find_element_by_name('username').send_keys(credentials['username'])
            self.driver.find_element_by_name('password').send_keys(credentials['password'])
            self.driver.find_element_by_css_selector('button[class="gwt-Button"]').click()
        else:
            print("Login credentials not provided - using guest account.")
