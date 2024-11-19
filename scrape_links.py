import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Import tqdm for progress bar

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

        result = []
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

            result.append({
                "title": title,
                "date": date,
                "categories": categories,
                "download_links": download_links,
                "screenshots": screenshots,
                "features": features
            })
        
        return result

    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout_seconds} seconds.")
        return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# Function to scrape multiple pages concurrently
def scrape_pages_concurrently(start_page, end_page):
    data = {}
    url = lambda x: f"https://fitgirl-repacks.site/page/{x}"

    # Create a ThreadPoolExecutor for concurrent downloads
    with ThreadPoolExecutor() as executor:
        future_to_page = {executor.submit(scrape_links_with_text, url(i)): i for i in range(start_page, end_page)}

        # Initialize tqdm progress bar
        with tqdm(total=end_page - start_page, desc="Processing Pages") as pbar:
            # Iterate through completed futures
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    result = future.result()
                    if result:
                        data[page] = result
                except Exception as exc:
                    print(f"Page {page} generated an exception: {exc}")
                
                # Update the progress bar after each page is processed
                pbar.update(1)

    return data

if __name__ == "__main__":
    start_page = 1
    end_page = 535  # Adjust this range as needed

    # Call the function to scrape pages concurrently
    all_data = scrape_pages_concurrently(start_page, end_page)

    # Print the result (or save it as needed)
    for page, content in all_data.items():
        print(f"Page {page} - {len(content)} articles found.")
