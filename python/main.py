import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setting the options for the selenium browser
options = Options()
options.page_load_strategy = 'normal'
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
email_id = 'Your_linkedIn_email'
password_ = 'Your_linkedIn_password'
compititor_profile = "compitior profile"


# getting the data of compititors connections
def get_connection_data(profile):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api_key = 'Your_proxycurl_api_key'
    header_dic = {'Authorization': 'Bearer ' + api_key}
    params = {
        'url': f'https://www.linkedin.com/in/{profile}/',
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include',
        'inferred_salary': 'include',
        'personal_email': 'include',
        'personal_contact_number': 'include',
        'twitter_profile_id': 'include',
        'facebook_profile_id': 'include',
        'github_profile_id': 'include',
        'extra': 'include',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=header_dic)
    response.raise_for_status()
    return response.content


# getting the list of compititor connections
def track_connections():
    driver.get(
        'https://www.linkedin.com')
    # login
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Sign in'))).click()
    username = driver.find_element(By.ID, 'username')
    username.send_keys(email_id)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_)
    driver.find_element(By.CSS_SELECTOR, 'div button').click()
    time.sleep(15)
    driver.get(
        f"https://www.linkedin.com/in/{compititor_profile}/")  # type-in the link of compititor's linkedIn profile
    time.sleep(3)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/ul/li/a'))).click()
    time.sleep(3)

    conection_link = driver.find_elements(By.CSS_SELECTOR, 'div .entity-result__item a')
    time.sleep(4)
    links = [elem.get_attribute('href') for elem in
             conection_link]
    driver.quit()
    return links


links = track_connections()
print(links)
result = []
profile = []

for url in links:
    in_index = url.find('in/')
    question_mark_index = url.find('?')
    # Extract the desired parts of the URL
    result.append(url[in_index + 3:question_mark_index])
    print(result)
    data = get_connection_data(result)
    print(data)
    profile.append(data)
    # the api i used only gave me 2 req per minute, that's why i am taking a time pause of 60 secs
    time.sleep(60)

print(profile)
print(result)


# sending connection request to the connections
def connection_req():
    driver.get(
        'https://www.linkedin.com')
    # login
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Sign in'))).click()
    username = driver.find_element(By.ID, 'username')
    username.send_keys(email_id)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_)
    driver.find_element(By.CSS_SELECTOR, 'div button').click()
    time.sleep(3)
    for r in result:
        driver.get(
            f'https://www.linkedin.com/in/{r}/')
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="ember2617"]/span').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="ember1440"]').click()
        except:
            print("can't connect")
        else:
            print(f"request send successfully to {r}")
        finally:
            pass


connection_req()

# I haven't studied Natural Language Processing (NLP) yet, that's why i wasn't able to generate a hyper-personalized connection request.
# I will start learning natural language processing technique's as early as possible in future.
