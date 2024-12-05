import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import json

# The `HEADERS` dictionary in the provided Python code snippet is used to set custom headers for HTTP
# requests made using the `requests` library. Here's what each key in the `HEADERS` dictionary
# represents:
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_total_pages(url):
    """
    The function `get_total_pages` retrieves the total number of pages from a website's pagination
    section.
    
    :param url: The `get_total_pages` function you provided seems to be a Python function that extracts
    the total number of pages from a website's pagination section. It uses the `requests` library to
    make HTTP requests and `BeautifulSoup` for parsing HTML content
    :return: The function `get_total_pages(url)` returns the total number of pages found in the
    pagination section of the HTML content retrieved from the provided URL. If there is a pagination
    section with at least two anchor tags (`<a>`), it returns the integer value of the second-to-last
    anchor tag's text content. If there is no pagination section or if there are less than two anchor
    tags, it returns
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        if pagination_div := soup.find(
            'div', class_='pagination loop-pagination'
        ):
            a_tags = pagination_div.find_all('a')
            if len(a_tags) >= 2:
                return int(a_tags[-2].get_text(strip=True))
        return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 1

def scrape_links_with_text(url):
    """
    The function `scrape_links_with_text` scrapes information from articles on a webpage and returns a
    list of dictionaries containing various details like title, date, download links, screenshots,
    features, genres, companies, languages, and sizes.
    
    :param url: The function `scrape_links_with_text(url)` is designed to scrape information from a
    webpage given a URL. It uses the requests library to make a GET request to the URL and BeautifulSoup
    to parse the HTML content
    :return: The function `scrape_links_with_text(url)` returns a list of dictionaries, where each
    dictionary represents information about articles scraped from the provided URL. The dictionaries
    contain details such as the article title, date, download links, screenshots, features, genres,
    companies, languages, original size, and repack size. If an error occurs during the scraping
    process, an empty list is returned.
    """
    timeout_seconds = 10

    try:
        return _extracted_from_scrape_links_with_text_19(url, timeout_seconds)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"An error occurred: {e}")
        return []


# TODO Rename this here and in `scrape_links_with_text`
def _extracted_from_scrape_links_with_text_19(url, timeout_seconds):
    response = requests.get(url, headers=HEADERS, timeout=timeout_seconds)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')

    result = []
    for article in articles:
        title = article.find('h1', class_='entry-title').get_text(strip=True)
        if "Upcoming Repacks" in title:
            continue

        date = article.find('time', class_='entry-date')['datetime']
        download_links = [a['href'] for a in article.select('ul li a') if 'href' in a.attrs]
        screenshots = [img['src'] for img in article.select('h3 + p img')]
        features = [li.get_text(strip=True) for li in article.select('h3 + ul li')]

        stronk = article.select_one("div p").find_all('strong')
        genres, companies, languages, original_sizes, repack_sizes = "", "", "", "", ""

        if stronk:
            genres = stronk[0].get_text(strip=True).split(",")
            companies = stronk[1].get_text(strip=True).split(",")
            languages = stronk[2].get_text(strip=True).split("/")
            original_sizes = stronk[-2].get_text(strip=True)
            repack_sizes = stronk[-1].get_text(strip=True)

        result.append({
            "title": title,
            "date": date,
            "download_links": download_links,
            "screenshots": screenshots,
            "features": features,
            "genre": genres,
            "companies": companies,
            "languages": languages,
            "original_size": original_sizes,
            "repack_size": repack_sizes,
        })

    return result

def scrape_pages_concurrently(start_page, end_page):
    """
    The function `scrape_pages_concurrently` scrapes links with text from multiple pages concurrently
    using ThreadPoolExecutor and tqdm for progress tracking.
    
    :param start_page: The `start_page` parameter in the `scrape_pages_concurrently` function represents
    the starting page number from which you want to begin scraping data. This function is designed to
    scrape multiple pages concurrently, starting from the specified `start_page` and ending at the
    `end_page`
    :param end_page: The `end_page` parameter in the `scrape_pages_concurrently` function represents the
    page number up to which you want to scrape data from the website. This function will scrape data
    from the start_page up to (but not including) the end_page
    :return: The function `scrape_pages_concurrently` returns a list of data collected from scraping
    multiple pages concurrently within the specified range from `start_page` to `end_page`.
    """
    data = []
    url = lambda x: f"https://fitgirl-repacks.site/page/{x}"

    with ThreadPoolExecutor() as executor:
        future_to_page = {executor.submit(scrape_links_with_text, url(i)): i for i in range(start_page, end_page)}

        with tqdm(total=end_page - start_page, desc="Processing Pages") as pbar:
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    if result := future.result():
                        data += result
                except Exception as exc:
                    print(f"Page {page} generated an exception: {exc}")

                pbar.update(1)

    return data

def save_data_to_json(data, filename='data.json'):
    """
    The function `save_data_to_json` saves data to a JSON file with specified filename in a
    human-readable format.
    
    :param data: The `data` parameter in the `save_data_to_json` function represents the Python data
    that you want to save to a JSON file. This data can be a dictionary, list, string, integer, float,
    or any other valid Python data type that can be serialized to JSON format
    :param filename: The `filename` parameter in the `save_data_to_json` function is a string that
    represents the name of the file where the data will be saved in JSON format. By default, if no
    filename is provided when calling the function, it will save the data to a file named 'data.json',
    defaults to data.json (optional)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    base_url = "https://fitgirl-repacks.site/page/2"
    total_pages = get_total_pages(base_url)
    print(f"Total pages to scrape: {total_pages}")

    start_page = 1
    end_page = total_pages + 1

    all_data = scrape_pages_concurrently(start_page, end_page)
    save_data_to_json(all_data)

    print("Data saved to 'data.json'.")
