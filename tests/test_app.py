import re
import random

import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skip
def test_playwright_in_title(page: Page):
    page.goto(url='https:///playwright.dev')
    expect(page).to_have_title(re.compile('Playwright'))

@pytest.mark.skip # only_browser("chromium")
def test_can_add_a_new_task(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.locator("html").click()
    page.locator("#task_name").click()
    rand_int = random.randint(1,100)
    page.locator("#task_name").fill(f"item {rand_int}")
    page.get_by_role("button", name="Add Task").click()

    expect(page.locator('.task-list')).to_contain_text(f'item {rand_int}')

@pytest.mark.only_browser("chromium")
def test_can_enter_task(page: Page):
    page.goto("http://127.0.0.1:5000/")
    for x in range(10):
        page.get_by_test_id('task').fill(f'Entering task number #{x}')
        page.get_by_role("button", name="Add Task").click()

    # expect(page.locator('tr:has-text("Enter task number #1')).to_have_text('Enter task number #1')
    expect(page.locator('td:has-text("Entering task number #0")')).to_contain_text('Entering task number #0')
    