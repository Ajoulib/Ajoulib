from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging

service = Service("C:\\Users\\kai10\\Downloads\\chromedriver")


def bookkeyword(bookname):
    # keyword = input("책이름을입력하시오:")
    # WebDriver 초기화
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # Create a WebDriver instance with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 웹 페이지 열기
        url = "https://book.interpark.com/"
        driver.get(url)

        # 책 이름 입력
        search_box = driver.find_element(By.ID, "query")
        search_box.send_keys(bookname)

        # Enter 키 눌러 검색
        search_box.send_keys(Keys.RETURN)

        # 기다리는 동안 로직 추가 가능
        # ...

        # 검색 결과 페이지에서 정보 가져오기
        title = (
            driver.find_element(By.CLASS_NAME, "tit")
            .find_element(By.TAG_NAME, "a")
            .text
        )
        link_url = (
            driver.find_element(By.CLASS_NAME, "tit")
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )

        # 가져온 정보 출력
        print("Title:", title)
        print("Link:", link_url)

    except Exception as e:
        print(f"An error occurred: {e}")
    book_info = {
        "title": title,
        "INTRO": "없음",  # 여기에 목차 내용을 추가
        "TB": "없음",  # 여기에 소개 내용을 추가
    }
    retry_count = 2
    while retry_count > 0:
        try:
            # print("들어감")
            driver.get(link_url)
            # time.sleep(0.5)
            html = driver.page_source
            # 다음으로 진행하는 코드 추가

        except UnexpectedAlertPresentException:
            retry_count -= 1
            continue
        soup = BeautifulSoup(html, "html.parser")
        bookintroduce = soup.find("h3", class_="detailTitle", string="책소개")
        if bookintroduce == None:
            retry_count -= 1
            continue
        detail_introduce = bookintroduce.find_next("div", class_="detail_txtContent")
        if detail_introduce == None:
            retry_count -= 1
            continue
        bookintro = detail_introduce.get_text(strip=True).replace("\n", "")
        if bookintro == None:
            retry_count -= 1
            continue
        book_info["INTRO"] = bookintro
        toc_heading = soup.find("h3", class_="detailTitle", string="목차")
        if toc_heading == None:
            retry_count -= 1
            continue
        detail_txtContent = toc_heading.find_next("div", class_="detail_txtContent")
        if detail_txtContent == None:
            retry_count -= 1
            continue
        table_of_contents = detail_txtContent.get_text(strip=True).replace("\n", "")
        if table_of_contents is not None:
            # table_of_contents가 비어있지 않으면 업데이트하고 반복문 탈출
            book_info["TB"] = table_of_contents

            break

    driver.quit()
    return book_info


# # 웹 드라이버 종료
# if __name__ == "__main__":
#     bookname = input("책제목입력")
#     bookkey=bookkeyword(bookname)
