from pages.login_page import LoginPage

def test_valid_login(page):

    login = LoginPage(page)

    login.login(
        "https://accounts-staging.hexnode.com/login/",
        "yageshwaran.saravanan@mitsogo.com",
        "Tryhard1!"
    )

    # assert "dashboard" in page.url
    