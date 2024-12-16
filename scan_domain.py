import ipaddress
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import warnings
import argparse

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def check_domain(ip, domain, title_match):
    urls = [f"https://{ip}"]
    headers = {"Host": domain}
    
    for url in urls:
        with requests.Session() as session: 
            try:
                response = session.get(url, headers=headers, timeout=5, verify=False, allow_redirects=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title and soup.title.string else "NOT FOUND"
                    
                    if title_match in title:
                        print(f"\nDomain {domain} found on {ip} with matching title: '{title}'")
                        return True
            except requests.exceptions.RequestException:
                pass
    return False

def generate_ips(ip_blocks):
    for block in ip_blocks:
        for ip in ipaddress.IPv4Network(block):
            yield str(ip)

def main():
    parser = argparse.ArgumentParser(description="Scan a range of IPs to check if a domain is hosted on them.")
    parser.add_argument("domain", help="Domain to search for (e.g., example.com)")
    parser.add_argument("title_match", help="Partial or full title text to match in the webpage's title")
    parser.add_argument("ip_blocks", nargs="+", help="List of IP blocks (CIDR notation, e.g., 192.168.0.0/24)")
    
    args = parser.parse_args()

    ips_to_check = list(generate_ips(args.ip_blocks))

    with ThreadPoolExecutor(max_workers=500) as executor:
        with tqdm(total=len(ips_to_check), desc="Scanning IPs", unit="IP") as progress:
            futures = {executor.submit(check_domain, ip, args.domain, args.title_match): ip for ip in ips_to_check}
            
            for future in as_completed(futures):
                future.result()
                progress.update(1)

if __name__ == "__main__":
    main()
