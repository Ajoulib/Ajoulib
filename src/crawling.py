from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException

max_page_num = 10
# max_page_num = 2
dataset = []


def extract_year(text):
    start_index = text.find("('82','") + len("('82','")
    end_index = text.find("000','yearSch')")
    if start_index != -1 and end_index != -1:
        year = text[start_index:end_index]
        return year
    return None


service = Service("/home/kai/Downloads/데이터마이닝프로젝트/chromedriver")
driver = webdriver.Chrome()

url = "https://book.interpark.com/bookPark/html/book.html"
driver.get(url)
time.sleep(1)

# 베스트셀러 탭으로 이동
element = driver.find_element(By.CLASS_NAME, "gnbleft.n1")
element.click()
time.sleep(2)
annual_tab = driver.find_element(By.ID, "cateTabId4")
annual_tab.click()
time.sleep(1)

# category id= 소설-cateBookIdSub028005 // 시/에세이-cateBookIdSub028037
name = "novel"
novel = "li#cateBookIdSub028005 a"
poem_essay = "li#cateBookIdSub028037 a"
economics_management = "li#cateBookIdSub028003 a"
selfdevelopment = "li#cateBookIdSub028016 a"
socialscience = "li#cateBookIdSub028007 a"
history_culture = "li#cateBookIdSub028010 a"
art_popculture = "li#cateBookIdSub028011 a"
humanity = "li#cateBookIdSub028013 a"
nature_science = "li#cateBookIdSub028017 a"
religion_epidemiology = "li#cateBookIdSub028020 a"
infant = "li#cateBookIdSub028031 a"
child = "li#cateBookIdSub028008 a"
home_life = "li#cateBookIdSub028001 a"
teen = "li#cateBookIdSub028021 a"
elementarylearning = "li#cateBookIdSub028024 a"
computer_internet = "li#cateBookIdSub028023 a"
travel = "li#cateBookIdSub028009 a"
hobby_leisure = "li#cateBookIdSub028022 a"
health_beauty = "li#cateBookIdSub028002 a"

datenum = 0
category_link = driver.find_element(By.CSS_SELECTOR, economics_management)
category_link.click()
time.sleep(1)

period_selector = driver.find_element(By.ID, "periodSelectorId")
year_links = period_selector.find_elements(By.TAG_NAME, "li")
dates = []
time.sleep(1)
for year_link in year_links:
    # 각 년도에 대한 a 태그 찾기
    year_link_a = year_link.find_element(By.TAG_NAME, "a")
    dates.append(year_link_a.get_attribute("href"))

for date in dates:
    print("년도", date)
    datenum += 1
    if datenum == 4:
        break
    driver.execute_script(date)
    annual_tab = driver.find_element(By.ID, "cateTabId4")
    time.sleep(0.5)
    annual_tab.click()
    num_list_locator = (By.CLASS_NAME, "numList")
    page_span = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(num_list_locator)
    )
    page_links = page_span.find_elements(By.TAG_NAME, "a")

    # 페이지 숫자를 저장할 리스트
    page_numbers = []
    csv_file_path = "bookdata.csv"

    # 페이지 번호를 추출합니다.
    for link in page_links:
        page_number = int(link.text)
        page_numbers.append(page_number)
    print(page_numbers)
    # 10 페이지까지의 정보를 가져오기
    rank = 0
    current_url = driver.current_url
    print(current_url)
    for page_number in range(1, min(max(page_numbers), 2)):
        # 페이지 번호 클릭
        # page_link = driver.find_element(By.XPATH, f"//a[text()='{page_number}']")
        # print(page_link)
        wait = WebDriverWait(driver, 10)  # 최대 10초까지 대기
        page_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{page_number}']"))
        )
        page_link.click()
        time.sleep(0.5)  # 페이지가 로드될 때까지 대기

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        book_items = soup.find_all("div", class_="listItem singleType")
        year = extract_year(date)
        for item in book_items:
            rank += 1
            title = item.find("div", class_="itemName").strong.text.strip()
            author = item.find("span", class_="author").text.strip()
            url = item.find("a", href=True)["href"]
            dataset.append([year, rank, title, author, url, None, None])
            # driver.get("https://book.interpark.com" + url)
            # time.sleep(0.5)
            # driver.back()
            # html = driver.page_source
            # soup = BeautifulSoup(html, "html.parser")
            # toc_heading = soup.find("h3", class_="detailTitle", text="목차")

            # if toc_heading:
            #     # h3 태그의 부모인 detail_txtContent 찾기
            #     detail_txtContent = toc_heading.find_next(
            #         "div", class_="detail_txtContent"
            #     )
            #     table_of_contents =path detail_txtContent.get_text(strip=True)


book_df = pd.DataFrame(
    dataset, columns=["Year", "Rank", "Title", "Author", "URL", "INTRO", "TB"]
)
for index, row in book_df.iterrows():
    current_url = row["URL"]
    try:
        driver.get("https://book.interpark.com" + current_url)
        # time.sleep(0.5)
        html = driver.page_source
        # 다음으로 진행하는 코드 추가

    except UnexpectedAlertPresentException:
        print("Unexpected Alert: Skipping to the next iteration.")
        continue
    soup = BeautifulSoup(html, "html.parser")
    bookintroduce = soup.find("h3", class_="detailTitle", text="책소개")
    if bookintroduce:
        detail_introduce = bookintroduce.find_next("div", class_="detail_txtContent")
        bookintro = detail_introduce.get_text(strip=True)
        print(bookintro)
        book_df.loc[index, "INTRO"] = bookintro

    toc_heading = soup.find("h3", class_="detailTitle", text="목차")
    if toc_heading:
        # h3 태그의 부모인 detail_txtContent 찾기
        detail_txtContent = toc_heading.find_next("div", class_="detail_txtContent")
        table_of_contents = detail_txtContent.get_text(strip=True)
        print(table_of_contents)

        # DataFrame에서 해당 URL에 해당하는 행의 'TB' 값을 업데이트
        book_df.loc[index, "TB"] = table_of_contents


# book_df.to_csv(csv_file_path, index=False)
book_df = book_df.drop("URL", axis=1)
csv_file_path1 = name + "FINALbookdata.csv"
book_df.to_csv(csv_file_path1, index=False)

# Chrome 드라이버 종료

driver.quit()
