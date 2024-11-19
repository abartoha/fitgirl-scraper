import requests
from lxml import html

def scrape_links_with_text(url, xpath):
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

        # Parse the HTML content
        tree = html.fromstring(response.content)

        # Extract links and their inner text based on XPath
        elements = tree.xpath(f"{xpath}//li//a")
        links_with_text = {
            (element.text_content() or "No text").strip(): element.get("href")
            for element in elements
        }

        return links_with_text

    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout_seconds} seconds.")
        return {}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

# Example usage
url = "https://fitgirl-repacks.site/"
xpath = '//*[@id="post-71473"]/div[2]/ul[28]'
links_with_text = scrape_links_with_text(url, xpath)

print(f"\nFound {len(links_with_text)} links with inner text:")
for text, link in links_with_text.items():
    print(f"Text: {text}\nLink: {link}\n")
