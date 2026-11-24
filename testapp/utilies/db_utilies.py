from django.db import transaction
from config import SCREENSHOT_DIR
from pathlib import Path
from asgiref.sync import sync_to_async

async def take_screenshot(page, step_name, screenshot_name="screenshot.png"):

    screenshot_dir = Path(SCREENSHOT_DIR) / step_name
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / screenshot_name

    # print("Screenshot function called!")
    # print("Saving location:", screenshot_path)

    await page.screenshot(path=str(screenshot_path), full_page=True)

    # print("Screenshot saved successfully!")
    # print("File exists:", screenshot_path.exists())

    return screenshot_path

@sync_to_async
def save_test_data(model_name,test_result):
    """save test result in the database"""


    if not isinstance(test_result,dict):
        raise TypeError(f"Test result must be dictionary .")

    with transaction.atomic():
        save_data=model_name.objects.create(**test_result)

    return save_data
