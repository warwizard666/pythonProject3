import bs4
import requests
from fake_headers import Headers
import json

def get_headers():
    return Headers(os="win", browser="firefox").generate()

response = requests.get("https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter", headers=get_headers())

main_html_data = response.text

soup = bs4.BeautifulSoup(main_html_data, features="lxml")

def parse_vacancies(soup):
    vacancies = soup.find_all("div", class_="vacancy-search-item__card")

    vacancy_list = []

    for vacancy in vacancies:
        link = vacancy.find("a", class_='bloko-link').get('href')
        vacancy_name = vacancy.find("a", class_='bloko-link').get_text()
        company = vacancy.find("span", class_="company-info-text--vgvZouLtf8jwBmaD1xgp").get_text()
        salary_element = vacancy.find("div", class_='compensation-labels--uUto71l5gcnhU2I8TZmz').find("span", class_="bloko-text")
        salary = salary_element.text.strip() if salary_element else "Уровень дохода не указан"
        city = vacancy.find("div", class_="info-section--N695JG77kqwzxWAnSePt").find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni").text.strip()
        vacancy_list.append({
            "вакансия": vacancy_name,
            "ссылка": link,
            "зарплата": salary,
            "название компании": company,
            "город": city
        })
    return vacancy_list
vacancy_list = parse_vacancies(soup)
with open('vacancys.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, ensure_ascii=False, indent=5)
