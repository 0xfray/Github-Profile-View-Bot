from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import time
import random

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.page_load_strategy = "eager"

    service = Service("Path---To---Chrome---Driver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_random_user_agent():
    ua = UserAgent()
    try:
        return ua.random
    except Exception:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def load_page(driver, url):
    try:
        driver.get(url)
        print(f"Page loaded: {url}")
    except Exception as e:
        print(f"Error loading page: {e}")


def task(url, thread_id):
    driver = setup_driver()
    try:
        request_count = 0
        while True:
            user_agent = get_random_user_agent()
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
            print(f"[Thread-{thread_id}] Using User-Agent: {user_agent}")


            load_page(driver, url)
            request_count += 1
            print(f"[Thread-{thread_id}] Pages loaded: {request_count}")

            delay = random.uniform(0.1, 0.4)
            time.sleep(delay)
    finally:
        driver.quit()


def main():
    url = "https://github.com/0xfray" #change to your profile
    num_threads = 5 #number of threads 

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            executor.submit(task, url, i)


if __name__ == "__main__":
    main()
