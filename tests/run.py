import random
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, timeout=3000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5000/")
    for _ in range(20):
        page.get_by_test_id('task').fill(f'Entering task number #{random.randint(1,100)}')
        page.get_by_role("button", name="Add Task").click()

    # ---------------------
    page.wait_for_timeout(5000) 
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
