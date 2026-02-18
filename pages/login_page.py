from locators.login_locators import LoginLocators

class LoginPage:
    def __init__(self, page):
        self.page = page

    def open_login_page(self, url):
        self.page.goto(url)

    def enter_username(self, username):
        self.page.fill(LoginLocators.USERNAME_INPUT , username)

    def click_continue(self):
        self.page.click(LoginLocators.CONTINUE_BUTTON)   

    def enter_password(self, password):
        self.page.fill(LoginLocators.PASSWORD_INPUT , password)

    def click_login(self):
        self.page.click(LoginLocators.SIGNIN_BUTTON)

    def login(self, url, username, password):
        self.open_login_page(url)
        self.enter_username(username)
        self.click_continue()
        self.enter_password(password)
        self.click_login()

