from bs4 import BeautifulSoup
import requests
import re
from fake_useragent import UserAgent

from .mod import Resume 


head = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) Chrome/126.0.0.0 Mobile Safari/537.36"
}


def fetch_resume_data(query='python', min_salary=None, m=None, area=1, page_size=20):
    ua = UserAgent()
    page = 0
    all_resumes = []

    while True:
        url = f"https://hh.ru/search/resume?area={area}&exp_period=all_time&logic=normal&" \
              f"no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&" \
              f"search_period=0&text={query}&items_on_page={page_size}&page={page}"
        print(f"Ищем вакансии: {url}")

        response = requests.get(url, headers={'User-Agent': ua.chrome})
        print(f"Response status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'lxml')
        urls = soup.find_all('a', {'data-qa': "serp-item__title", 'class': "bloko-link"})

        if not urls:
            break

        for url in urls:
            resume_info = {}
            href = 'https://hh.ru/' + url.attrs['href']
            print(f"Ищем резюме: {href}")

            response = requests.get(href, headers={'User-Agent': ua.chrome})
            print(f"Response status code for resume details: {response.status_code}")

            soup = BeautifulSoup(response.text, 'lxml')

            salary_obj = soup.find('span', {'class': 'resume-block__salary'})
            if salary_obj:
                salary_text = salary_obj.text.strip()
                salary_digits = re.findall(r'\d+', salary_text)
                salary = int(''.join(salary_digits))
            else:
                salary = None

            if min_salary and salary is not None and salary < min_salary:
                print(f"Skipping resume '{href}' due to salary requirement.")
                continue

            title_obj = soup.find('span', {'class': 'resume-block__title-text'})
            job_title = title_obj.text.strip() if title_obj else 'Не указано'

            print(f"Job title: {job_title}")
            print(f"Salary: {salary}")

            try:
                if salary is None and min_salary:
                    print(f"Skipping resume '{href}' due to missing salary.")
                    continue

                resume = Resume(
                    title=job_title,
                    salary=salary if salary is not None else 0,  
                )
                resume.save()
                print("Resume saved to database.")
                all_resumes.append(resume)
            except Exception as e:
                print(f"Error saving resume to database: {e}")

        page += 1

    return all_resumes


























