import requests
from bs4 import BeautifulSoup

def scrape_links_with_text(url):
    # Custom headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    timeout_seconds = 10  # Define timeout in seconds

    try:
        # Send HTTP GET request with timeout
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            # Extract the title
            title = article.find('h1', class_='entry-title').get_text(strip=True)

            # Extract the publication date
            date = article.find('time', class_='entry-date')['datetime']

            # Extract the categories
            categories = [a.get_text(strip=True) for a in article.select('span.cat-links a')]

            # Extract download links
            download_links = [a['href'] for a in article.select('ul li a') if 'href' in a.attrs]

            # Extract screenshots
            screenshots = [img['src'] for img in article.select('h3 + p img')]

            # Repacks Features
            features = [li.get_text(strip=True) for li in article.select('h3 + ul li')]

            print("Title:", title)
            print("Date Published:", date)
            print("Categories:", len(categories))
            print("Download Links:", len(download_links))
            print("Screenshots:", len(screenshots))
            print("Features:", len(features))
        return title, [date, categories, download_links, screenshots, features]

    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout_seconds} seconds.")
        return {}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

# Example usage

if __name__ == "__main__":
    data = {}
    url = lambda x: f"https://fitgirl-repacks.site/page/{x}"
    
    for i in range(0,535):
        k, v = scrape_links_with_text(url(i+1))
        data[k] = v

