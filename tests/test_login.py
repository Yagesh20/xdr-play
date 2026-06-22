from pages.login_page import LoginPage


def test_login_success(page):
    login = LoginPage(page)

    login.login()

    print("Final URL:", page.url)