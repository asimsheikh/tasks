from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("row", name="first task").get_by_role("link", name="edit task").click()
    page.locator("html").click()
    page.locator("#task_name").click()
    page.locator("#task_name").fill("first task changed")
    page.locator("#task_completed").click()
    page.locator("#task_completed").fill("False")
    page.locator("#task_completed").press("Tab")
    page.locator("#task_pomodoros").fill("14")
    page.get_by_role("button", name="Save Task").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
