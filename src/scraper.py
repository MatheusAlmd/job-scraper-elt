import requests
from bs4 import BeautifulSoup

def get_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="card-content")

    vacancies = []

    for job in jobs:
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        location = job.find("p", class_="location").text.strip()

        # proteção contra erro
        if ", " in location:
            city, state = location.split(", ")
        else:
            city, state = location, ""

        vacancy = {
            "title": title,
            "company": company,
            "city": city,
            "state": state
        }

        vacancies.append(vacancy)

    return vacancies