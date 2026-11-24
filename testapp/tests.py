import random
from pathlib import Path
from playwright.async_api import async_playwright
from config import BROWSER,HEADLESS,SLOW_MO,DEFAULT_TIMEOUT,AIRBNB_BASE_URL
from testapp.utilies.db_utilies import take_screenshot
from testapp.models import Test01Model
from testapp.utilies.db_utilies import save_test_data
import calendar
from datetime import date,datetime
import re
from playwright.async_api import expect
from urllib.parse import urlparse, parse_qs
TOP_20_COUNTRIES=[
    "Bangladesh",
    "Malaysia",
    "Thailand",
    "Canada",
    "Bangladesh",
    "United Arab Emirates",
    "Thailand",
    "Sri Lanka",
    "NY",
    "Canada",
    "France",
    "Islands",
    "Canada",
    "Malaysia",
    "Thailand",
    "Thailand",
    "United Kingdom",
    "Saudi Arabia",
    "Türkiye",
    "Nepal",

]


async def load_browser():

    playwright= await async_playwright().start()
    browser_type=getattr(playwright,BROWSER)
    browser=await browser_type.launch(headless=HEADLESS,slow_mo=SLOW_MO)

    context=await browser.new_context()
    page=await context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)

    return playwright,browser,context,page

async def dismiss_active_modal(page, timeout: int = 3000) -> bool:
  modal = page.locator('[role="dialog"][aria-modal="true"]').first

  try:
    await modal.wait_for(state="visible", timeout=timeout)
  except Exception:
    return False

  
  close_patterns = re.compile(r"^(close|dismiss|got it|ok|okay|no thanks|skip)$", re.I)
  close_btn = modal.get_by_role("button", name=close_patterns).first

  if await close_btn.count() > 0 and await close_btn.is_visible():
    await close_btn.click()
  else:
    await page.keyboard.press("Escape")
  try:
    await modal.wait_for(state="hidden", timeout=2000)
  except Exception:
    await page.keyboard.press("Escape")
    await modal.wait_for(state="hidden", timeout=2000)

  return True


async def step1(context,page):
    

    homepage_load=False
    cookies_cleared=False
    local_storage_cleared=False
    selected_country=""
    

 
    await context.clear_cookies()
    cookies_cleared=True
    if cookies_cleared:
        results={
            "test_cases":"Verify cookies cleared",
            "url":AIRBNB_BASE_URL,
            "passed":cookies_cleared,
            "comment": f"Cookies cleared sucessfully!",
        }
        await save_test_data(Test01Model,results)

          
        

    await page.goto(AIRBNB_BASE_URL, wait_until="domcontentloaded")
    await dismiss_active_modal(page, timeout=3000)
    assert "airbnb.com" in page.url
    homepage_load=True
    screenshot_path=  await take_screenshot(page,"homepage_load_test","homepage_load.png")
    if homepage_load:
        results={
            "test_cases":"Verify that the homepage loads properly ",
            "url":AIRBNB_BASE_URL,
            "passed":homepage_load,
            "comment": f"Home page loaded sucessfully !",
        }
        await save_test_data(Test01Model,results)


    await page.evaluate("""
    ()=>{
        localStorage.clear();
        sessionStorage.clear();
       
    }""")
    local_storage_cleared=True
    if local_storage_cleared:
        results={
            "test_cases":"Verify that local storage is cleared properly",
            "url":AIRBNB_BASE_URL,
            "passed":local_storage_cleared,
            "comment": f"local storage is cleared successfully !", 
        }
        await save_test_data(Test01Model,results)
        

    selected_country=random.choice(TOP_20_COUNTRIES)
    results={
        "test_cases":" Verify country is selected Randomly!",
        "url":AIRBNB_BASE_URL,
        "passed":"True",
        "comment": f"{selected_country} is selected!",
        
    }
    await save_test_data(Test01Model,results)


    await page.wait_for_load_state("domcontentloaded")
    destination_input=page.get_by_placeholder("Search destinations",exact=False)
    await destination_input.wait_for(state="visible", timeout=10000)
    await destination_input.fill(selected_country)
    screenshot_path=  await take_screenshot(page,"search_country","search_country.png")

    return selected_country


async def step2(page,search_location):
    
    auto_suggestions_list= False
    valid_display_list= True
    show_google_map_icon= True
    show_location_text= True
    all_suggested_location=[]

    await page.wait_for_load_state("domcontentloaded")
    await dismiss_active_modal(page, timeout=3000)
    destination_input=page.get_by_placeholder("Search destinations",exact=False)
    await destination_input.wait_for(state="visible", timeout=10000)
    await destination_input.fill(search_location)
    suggestions = page.locator('[id^="bigsearch-query-location-suggestion-"]')

    suggestion_count=await suggestions.count()
    for i in range(suggestion_count):
        location=await suggestions.nth(i).inner_text()
        all_suggested_location.append(location)
        if search_location.lower() not in location.lower():
            valid_display_list=False
            break
    if valid_display_list:
        results={
            "test_cases":"Verify the displayed suggestions are relevant to the entered location",
            "url":AIRBNB_BASE_URL,
            "passed":valid_display_list,
            "comment": f"Ensured suggestions are relevant to the entered location",
        }
        await save_test_data(Test01Model,results)

    map_icons=page.locator('div.p1183tkl.atm_vy_1osqo2v.dir.dir-ltr span div svg')
    icon_count = await map_icons.count()
    # print(icon_count)
    for i in range(icon_count):
        icon=map_icons.nth(i)
        if not await icon.is_visible():
            show_google_map_icon=False
            print(f"{i}th location has not google map icon")
            break
    if show_google_map_icon:
        results={
            "test_cases":"Verify each suggestion shows a Google Map icon",
            "url":AIRBNB_BASE_URL,
            "passed":show_google_map_icon,
            "comment": f"Ensured each suggestion shows a Google Map icon",
        }
        await save_test_data(Test01Model,results)

        
    location_text=page.locator('div.tr7xgkn.atm_j_1h6ojuz.atm_ks_15vqwwr.dir.dir-ltr')
    text_count=await location_text.count()
    # print(text_count)
    for i in range(text_count):
        text=location_text.nth(i)
        if not await text.is_visible():
            show_location_text=False
            print(f"{i}th location has no visible location name")

    if show_location_text:
        results={
            "test_cases":"Verify each suggestion shows location text",
            "url":AIRBNB_BASE_URL,
            "passed":show_location_text,
            "comment": f"Ensured each suggestion shows location text",
        }
        await save_test_data(Test01Model,results)

        # print(show_google_map_icon,show_location_text,all_suggested_location)


async def step3(page,selected_country):

    date_picker_modals_opens= True

    await step2(page,selected_country)
    suggestions=page.locator('[id^="bigsearch-query-location-suggestion-"]')
    location = suggestions.first
    selected_location = await location.inner_text()
    await location.click()
    
    date_modals=page.locator('div.piqlc25.atm_9s_1txwivl.atm_fc_1h6ojuz.atm_vy_1osqo2v.atm_e2_1osqo2v.dir.dir-ltr')
    modals_count=await date_modals.count()

    for i in range(modals_count):
        modal=date_modals.nth(i)
        if not await modal.is_visible():
            date_picker_modals_opens=False
            break


    results = {
        "test_cases": "Verify date picker modal opens after selecting a location",
        "url": AIRBNB_BASE_URL,
        "passed": date_picker_modals_opens,
        "comment": "Date picker modals opened successfully!" if date_picker_modals_opens else "Date picker modals did not open!"
    }
    await save_test_data(Test01Model, results)
        

    next_month_btn=page.get_by_label('Move forward to switch to the next month.')
    click_random=random.randint(3,8)
    for i in range(click_random):
        await next_month_btn.click()
        
    month_heading=page.locator('h2.h1d0twz0.atm_c8_exct8b.atm_g3_gktfv.atm_cs_1mexzig.atm_7l_hfv0h6.atm_vy_1osqo2v.atm_vb_glywfm.atm_h3_qslrf5.atm_gq_qslrf5.atm_r3_1h6ojuz.dir.dir-ltr')
    month_text=await month_heading.first.inner_text()
    month_date = datetime.strptime(month_text, "%B %Y")
    year = month_date.year
    month = month_date.month
    total_days = calendar.monthrange(year, month)[1]
    check_in_day = random.randint(1, total_days-1)
    check_in_date = date(year, month, check_in_day)
    check_out_day=random.randint(check_in_day+1,total_days)
    check_out_date = date(year, month, check_out_day)

    
    date_buttons = page.locator('button[aria-label]')
    print("Total date buttons:", await date_buttons.count())
    # check_in_label = check_in_date.strftime("%B %d, %Y")
    check_in_label=( f"{check_in_date.day}, "f"{check_in_date.strftime('%A, %B %Y')}")

    check_in_selected = False
    
    for i in range(await date_buttons.count()):
        button = date_buttons.nth(i)
        aria_label=await button.get_attribute('aria-label')
        if aria_label and check_in_label.lower() in aria_label.lower() and "available" in aria_label.lower() and await button.is_enabled() and await button.is_enabled():
            await button.click()
            check_in_selected=True
            break
        
    date_buttons = page.locator('button[aria-label]')
    check_out_label = (f"{check_out_date.day}, "f"{check_out_date.strftime('%A, %B %Y')}")
    check_out_selected = False
    for i in range(await date_buttons.count()):
        button = date_buttons.nth(i)
        aria_label=await button.get_attribute('aria-label')
        if aria_label and check_out_label.lower() in aria_label.lower() and "available" in aria_label.lower() and await button.is_enabled() and await button.is_enabled():
            await button.click()
            check_out_selected=True
            break
    
    print("Check-in selected:", check_in_selected)
    print("Check-out selected:", check_out_selected)

    dates_selected = check_in_selected and check_out_selected
    date_is_valid = (
        check_in_date >= date.today()
        and check_out_date > check_in_date
    )
    print("display dates are valid")
    # print(dates_selected)
    return {
     "selected_country": selected_country,
     "selected_location": selected_location,
     "check_in_date": check_in_date,
     "check_out_date": check_out_date,
     "dates_selected": dates_selected,
     "date_is_valid": date_is_valid,
    }  
   

    

async def step4(page, selected_data):

    guest_popup = False
    guest_display = False
    infants_display = False
    pets_display = False

  
    selected_location = selected_data["selected_location"]
    check_in_date = selected_data["check_in_date"]
    check_out_date = selected_data["check_out_date"]

    

    guest_input_field = page.get_by_role("button",name=re.compile(r"^Who", re.I))

    await guest_input_field.wait_for(state="visible",timeout=15000)

    await guest_input_field.click()

    guest_popup_page = page.locator(
        "div.pkny13m.atm_tw_n17gr9.atm_vy_1osqo2v"
        ".atm_e2_1osqo2v.atm_26_9yka83.atm_7i_1qlzsek.dir.dir-ltr"
    )

    await guest_popup_page.wait_for(state="visible",timeout=15000)

    guest_popup = await guest_popup_page.is_visible()

    adults_incre_btn = page.locator('[data-testid="stepper-adults-increase-button"]')
    children_incre_btn = page.locator('[data-testid="stepper-children-increase-button"]')
    infants_incre_btn = page.locator('[data-testid="stepper-infants-increase-button"]')
    pets_incre_btn = page.locator('[data-testid="stepper-pets-increase-button"]')

    random_num = random.randint(2, 5)

    for i in range(random_num):
        await adults_incre_btn.click()
        await children_incre_btn.click()
        await infants_incre_btn.click()
        await pets_incre_btn.click()

    
    adults_value = page.locator('[data-testid="stepper-adults-value"]')
    children_value = page.locator('[data-testid="stepper-children-value"]')
    infants_value = page.locator('[data-testid="stepper-infants-value"]')
    pets_value = page.locator('[data-testid="stepper-pets-value"]')

    adults = int(await adults_value.inner_text())
    children = int(await children_value.inner_text())
    infants = int(await infants_value.inner_text())
    pets = int(await pets_value.inner_text())

    
    selected_guests = adults + children

    expected_guests = (f"{selected_guests} guests" if selected_guests > 1 else f"{selected_guests} guest")
    expected_infants = (f"{infants} infants" if infants > 1 else f"{infants} infant")
    expected_pets = (f"{pets} pets"if pets > 1 else f"{pets} pet")

    
    try:
        await expect(guest_input_field).to_contain_text( expected_guests)
        guest_display = True
        await expect(guest_input_field).to_contain_text(expected_infants)
        infants_display = True
        await expect(guest_input_field).to_contain_text(expected_pets)
        pets_display = True
    except AssertionError:
        pass

   
    search_button = page.locator('[data-testid="structured-search-input-search-button"]')

    await search_button.click()

    print("Destination:", selected_location)
    print("Check-in:", check_in_date)
    print("Check-out:", check_out_date)
    print("Guests:", selected_guests)
    print("Infants:", infants)
    print("Pets:", pets)

    return {
        "guest_popup": guest_popup,
        "guest_display": selected_guests,
        "infants_display": infants,
        "pets_display": pets,
        "check_in_date":check_in_date,
        "check_out_date":check_out_date,

    }

async def step5(page,guest_date_results):
    search_page_visible=False
    date_field_visible=False
    guest_field_visible=False
    valid_date=False
    valid_guest=False
    valid_infants=False
    valid_pets=False

    await page.wait_for_load_state("domcontentloaded")
    await dismiss_active_modal(page, timeout=3000)
    search_page=page.locator('div[id="layout_container"]')
    await search_page.wait_for(state="visible",timeout=3000)
    search_page_visible=await search_page.is_visible()
    # print(search_page_visible)

    # date_buttons = page.locator('button[aria-label]')
    # print("Total date buttons:", await date_buttons.count())

    check_in_date=str(guest_date_results["check_in_date"])
    check_out_date=str(guest_date_results["check_out_date"])

    # expected_check_in = check_in_date.strftime("%b %-d")
    # expected_check_out = check_out_date.strftime("%b %-d")
    # # print(expected_check_in,expected_check_out)#Jul 20 Jul 24

    # expected_date_range = f"{expected_check_in} - {expected_check_out.split(' ')[1]}"
    # print(expected_date_range)

    date_button = page.get_by_test_id("little-search-date")
    await date_button.wait_for(state="visible", timeout=10000)

    date_value_locator = date_button.locator("div.f1wvjdh").first
    await date_value_locator.wait_for(state="visible", timeout=10000)
    date_field_visible = await date_value_locator.is_visible()
    print(date_field_visible)

    guests_button = page.get_by_test_id("little-search-guests")
    await guests_button.wait_for(state="visible", timeout=10000)

    guests_value_locator = guests_button.locator("div.f1wvjdh").first
    await guests_value_locator.wait_for(state="visible", timeout=10000)
    guest_field_visible = await guests_value_locator.is_visible()

    print(guest_field_visible)

    page_url=page.url
    print(page_url)
    parsed_url = urlparse(page_url)
    query_param=parse_qs(parsed_url.query)

    page_check_in_date=query_param.get("checkin",[None])[0]
    page_check_out_date=query_param.get("checkout",[None])[0]
    print(page_check_in_date)
    print(page_check_out_date)
    valid_date=((page_check_in_date==check_in_date) and (page_check_out_date==check_out_date))
    print(valid_date)

    guests=guest_date_results["guest_display"]
    infants=guest_date_results["infants_display"]
    pets=guest_date_results["pets_display"]

    page_guest=int(query_param.get("adults",[None])[0])
    page_guest+=int(query_param.get("children",[None])[0])
    page_infants=int(query_param.get("infants",[None])[0])
    page_pets=int(query_param.get("pets",[None])[0])

    valid_guest=(page_guest==guests)
    valid_infants=(page_infants==infants)
    valid_pets=(page_pets==pets)
    print(valid_guest,valid_infants,valid_pets)






async def main():

    playwright, browser, context, page = await load_browser()

    try:

        selected_country = await step1(context, page)
        print(selected_country)
        print(f"successfully tested  Step 1 and stored in database!")

        # selected_location = await step2(page,selected_country)
        # print(f"successfully tested  Step 2 and stored in database!")
        selected_data = await step3(page, selected_country)
        guest_date_results = await step4(page, selected_data)
        await step5(page,guest_date_results)


        # print("Country:", selected_country)
        # print("Final selected destination:", selected_location)

    finally:

        await browser.close()

        await playwright.stop()









    




   



