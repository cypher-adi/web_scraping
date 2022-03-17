from bs4 import BeautifulSoup
import requests
import csv
import sys

URL = "https://stackoverflow.com/questions/tagged"
PAGE_LIMIT = 1

def build_url(base_url=URL, topic='python', tab="newest", page=1, pagesize=15):
    return f"{base_url}/{topic}?tab={tab}&page={page}&pagesize={pagesize}" #https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize=15

def scrape_page(page=1):
    """
    Function to scrape a single page in stack overflow
    """
    if(len(sys.argv)>1):
        response = requests.get(build_url(page=page, topic=sys.argv[1]))
    else:
        response = requests.get(build_url(page=page))
    
    page_questions = []
    soup = BeautifulSoup(response.text, "html.parser")
    question_summary = soup.find_all("div", class_="s-post-summary")

    for summary in question_summary:
        question = summary.find(class_="s-link").text
        stats = summary.find_all("span", class_="s-post-summary--stats-item-number")
        vote_count = stats[0].text
        answers_count = stats[1].text
        view_count = stats[2].text

        page_questions.append({
            "question":  question,
            "answers": answers_count,
            "views": view_count,
            "votes": vote_count
        })
    
    return page_questions


def scrape():
    """
    Function to scrape to PAGE_LIMIT
    """
    questions = []
    for i in range(1, PAGE_LIMIT + 1):
        page_questions = scrape_page(i)
        questions.extend(page_questions)
    return questions

def export_data():
    data = scrape()
    with open("questions.csv", "w") as data_file:
        fieldnames = ["answers", "question", "views", "votes"]
        data_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for d in data:
            data_writer.writerow(d)
        print("Done")
        


if __name__ == "__main__":
    # from pprint import pprint
    # pprint(scrape())
    export_data()