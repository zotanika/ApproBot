from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
Configurations
"""
# Time interval for refreshing request list
REFRESH_INTERVAL = 5
# Place your actual Chrome profile to maintain auto-login
CHROME_PROFILE_PATH = "/path/to/your/chrome/profile"
SHIFTEE_LOGIN_PAGE = "https://shiftee.io/ko/accounts/login"
# Place actual URL to your page listing the approval requests
SHIFTEE_REQUESTS_PAGE = "https://shiftee.io/app/your/company/id/manager/requests"

"""
Browser ready
"""
options = Options()
# options.add_argument("--headless")
# options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
driver = webdriver.Chrome(options=options)
# Manual or automatic login and transit to the page listing approval requests
driver.get(SHIFTEE_LOGIN_PAGE)
input("로그인 후 Enter를 눌러주세요...")
driver.get(SHIFTEE_REQUESTS_PAGE)

"""
Run the approval bot
"""
def do_approve():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-approve"))
        )

        approve_buttons = driver.find_elements(By.CLASS_NAME, "btn-approve")
        print(f"{len(approve_buttons)}개의 승인 버튼을 발견했습니다.")

        for btn in approve_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", btn)
                print("승인 버튼을 클릭했습니다.")
                time.sleep(1)

                # Wait for appearing of modal window
                approve_modal_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '승인하기')]"))
                )
                approve_modal_btn.click()
                print("모달에서 '승인하기'를 클릭했습니다.")
                time.sleep(1)
            except Exception as e:
                print("개별 승인을 실패했습니다:", e)
    except Exception as e:
        print("발견된 승인 버튼이 없습니다:", e)

def main():
    while True:
        print("승인 요청이 있는지 확인하고 있습니다...")
        do_approve()
        print(f"{REFRESH_INTERVAL}초 후에 재확인합니다...\n")
        time.sleep(REFRESH_INTERVAL)
        driver.refresh()

try:
    main()
except KeyboardInterrupt:
    print("사용자가 강제 종료했습니다.")
finally:
    driver.quit()
