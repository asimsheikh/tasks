import random
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, timeout=3000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5000/")
    for x in range(10):
        page.get_by_test_id('task').fill(f'Entering task number #{x}')
        page.get_by_role("button", name="Add Task").click()

    # expect(page.locator('tr:has-text("Entering task number #0")')).to_be_visible()
    # ---------------------
    # page.wait_for_timeout(5000) 
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
