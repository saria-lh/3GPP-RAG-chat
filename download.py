import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url = 'https://www.etsi.org/deliver/'
is_pdf_link = lambda url: url.lower().endswith(".pdf")

def check_url(url, to_remove='/deliver/', visited=set()):
    if is_pdf_link(url):
        return

    print(f"Checking: {url}")
    print('..............')
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception:
        try:
            soup = BeautifulSoup(response.text, 'html5lib')  # or 'html5lib'
        except Exception:
            return

    links = soup.find_all('a')
    links = links[1:]
    links = links[::-1]

    # Extract the href attribute from each <a> tag
    for link in links:
        href = link.get('href')
        if href:
            url_end = href.replace(to_remove,'')
            to_remove+=url_end
            to_check=url+url_end
            full_url = urljoin(url, href)
            if full_url not in visited:
                visited.add(full_url)
                if is_pdf_link(full_url):
                    try:
                        download_pdf(full_url)
                    except Exception as e:
                        print(e)
                else:
                    check_url(full_url, '/deliver/', visited)
        to_remove='/deliver/'


def download_pdf(url, save_path='downloaded_pdfs/'):
    response = requests.get(url)
    file_name=url.rsplit('/', 1)[-1]
    save_path=save_path+file_name
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"PDF file from {url} saved.")

check_url(url)

    