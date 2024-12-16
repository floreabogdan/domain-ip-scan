
# Domain Scanner
This project helps in cybersecurity tasks by scanning IP ranges to identify the real server behind a domain, bypassing reverse proxies like Cloudflare. It matches the domain's title to confirm the correct server.

## Features
- Scans IPs in provided CIDR blocks.
- Checks if a specified domain is hosted on each IP.
- Matches a given string in the title of the webpage.
- Uses concurrent threads for faster scanning.
- Outputs results as it finds matches.

## Requirements
- Python 3.6 or higher
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

You can install these dependencies by running:

```bash
pip install requests beautifulsoup4 tqdm
```

## Usage

To use the script, run it from the command line with the following syntax:

```bash
python scan_domain.py <domain> <title_match> <ip_blocks...>
```

### Arguments:
- `<domain>`: The domain to search for (e.g., `example.com`).
- `<title_match>`: A partial or full title of the webpage you want to match (e.g., `"Example Title"`).
- `<ip_blocks...>`: One or more IP blocks in CIDR notation (e.g., `192.168.0.0/24 10.0.0.0/24`).

### Example:

```bash
python scan_domain.py example.com "Example Title" 192.168.0.0/24 10.0.0.0/24
```

This command will:
- Search for the domain `example.com`
- Look for the title `"Example Title"` on pages hosted on IPs in the ranges `192.168.0.0/24` and `10.0.0.0/24`.

### Example Output:

```plaintext
Domain example.com found on 192.168.0.10 with matching title: 'Example Title'
Domain example.com found on 10.0.0.5 with matching title: 'Example Title'
```

## How It Works:
1. The script takes the CIDR blocks provided and generates all IPs within those ranges.
2. For each IP, it makes an HTTP request to `https://<IP>` with the specified domain name as the `Host` header.
3. It checks the title of the page and compares it with the provided string.
4. If a match is found, it outputs the IP and the matching title.

### Notes:
- The script uses HTTPS to attempt a connection to each IP but does not verify SSL certificates due to potential security warnings from the IPs being scanned.
- The scanning is done concurrently using threads to speed up the process.
- The script supports scanning large IP ranges efficiently, using multi-threading to check many IPs at once.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
If you'd like to contribute to this project, feel free to fork it and submit a pull request. Any contributions or suggestions are welcome!

## Acknowledgements
- The `requests` library for handling HTTP requests.
- `beautifulsoup4` for parsing and extracting titles from HTML.
- `tqdm` for providing a progress bar.
- `argparse` for handling command-line arguments.
