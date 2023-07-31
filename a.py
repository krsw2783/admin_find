import argparse
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
requests.packages.urllib3.disable_warnings()
from urllib.parse import urljoin
def check_url_status(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
        response = requests.get(url, allow_redirects=True,verify=False,headers=headers)
        if response.status_code == 200 and len(response.content) > 10:
            if "ログイン" in response.text or "login" in response.text or "Login" in response.text or "Password" in response.text or "password" in response.text:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Error while checking URL {url}: {str(e)}")
        return False

def process_url(path, url_to_check):
    if "[]" in path:
        admin_path = unquote(path.replace('[', '').replace(']', '')).strip()
        parsed_url = urlparse(url_to_check)
        scheme = parsed_url.scheme
        domain_parts = parsed_url.netloc.split('.')
        if domain_parts[-2] in ['co', 'com', 'ac', 'or', 'go', 'ne']: # 2レベルTLDのリストを追加
            base_domain = '.'.join(domain_parts[-3:])
        else:
            base_domain = '.'.join(domain_parts[-2:])
        netloc = admin_path + base_domain
        path = parsed_url.path
        full_url = f"{scheme}://{netloc}{path}"
    else:
        full_url = urljoin(url_to_check,path.strip())
    status = check_url_status(full_url)
    if status:
        print(f"{full_url}は恐らくログイン場面ナリ")
    
def main():
    parser = argparse.ArgumentParser(description="Check URL status from a list of admin URLs.")
    parser.add_argument("-u", "--url", required=True, help="Base URL to check")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default is 10)")

    args = parser.parse_args()
    url_to_check = args.url
    num_threads = args.threads

    with open('adminlist.txt', 'r') as file:
        admin_paths = file.readlines()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for admin_path in admin_paths:
            executor.submit(process_url, admin_path, url_to_check)

if __name__ == "__main__":
    main()

