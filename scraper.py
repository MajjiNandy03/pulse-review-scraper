import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except:
        return None

def scrape_g2(company, start_date, end_date):
    reviews = []
    url = f"https://www.g2.com/products/{company}/reviews"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print("Invalid G2 company name")
        return reviews

    soup = BeautifulSoup(res.text, "html.parser")
    blocks = soup.find_all("div", class_="paper")

    for block in blocks:
        title = block.find("h3")
        desc = block.find("p")
        date_tag = block.find("time")

        if not (title and desc and date_tag):
            continue

        review_date = parse_date(date_tag.text.strip())
        if not review_date:
            continue

        if start_date <= review_date <= end_date:
            reviews.append({
                "title": title.text.strip(),
                "review": desc.text.strip(),
                "date": review_date.strftime("%Y-%m-%d"),
                "source": "G2"
            })

    return reviews

def scrape_capterra(company, start_date, end_date):
    reviews = []
    url = f"https://www.capterra.com/p/{company}/reviews/"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print("Invalid Capterra company name")
        return reviews

    soup = BeautifulSoup(res.text, "html.parser")
    blocks = soup.find_all("div", class_="review")

    for block in blocks:
        title = block.find("h3")
        desc = block.find("p")
        date_tag = block.find("time")

        if not (title and desc and date_tag):
            continue

        review_date = parse_date(date_tag.text.strip())
        if not review_date:
            continue

        if start_date <= review_date <= end_date:
            reviews.append({
                "title": title.text.strip(),
                "review": desc.text.strip(),
                "date": review_date.strftime("%Y-%m-%d"),
                "source": "Capterra"
            })

    return reviews

def scrape_trustradius(company, start_date, end_date):
    reviews = []
    url = f"https://www.trustradius.com/products/{company}/reviews"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print("Invalid TrustRadius company name")
        return reviews

    soup = BeautifulSoup(res.text, "html.parser")
    blocks = soup.find_all("div", class_="review")

    for block in blocks:
        title = block.find("h3")
        desc = block.find("p")
        date_tag = block.find("time")

        if not (title and desc and date_tag):
            continue

        review_date = parse_date(date_tag.text.strip())
        if not review_date:
            continue

        if start_date <= review_date <= end_date:
            reviews.append({
                "title": title.text.strip(),
                "review": desc.text.strip(),
                "date": review_date.strftime("%Y-%m-%d"),
                "source": "TrustRadius"
            })

    return reviews

def main():
    company = input("Enter company name (slug): ").strip()
    source = input("Source (g2 / capterra / trustradius): ").strip().lower()
    start = input("Start date (YYYY-MM-DD): ")
    end = input("End date (YYYY-MM-DD): ")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    if source == "g2":
        data = scrape_g2(company, start_date, end_date)
    elif source == "capterra":
        data = scrape_capterra(company, start_date, end_date)
    elif source == "trustradius":
        data = scrape_trustradius(company, start_date, end_date)
    else:
        print("Invalid source")
        return

    with open("sample_output.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Reviews saved to sample_output.json")

if __name__ == "__main__":
    main()
