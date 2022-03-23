from typing import List
import requests

import click

from config.api import company_search_url

def search_companies(company_name: str) -> List[dict]:
    """
    Search for a company name in screener.
    """
    url: str = f"{company_search_url}{company_name}"
    companies = requests.get(url).json()
    print(companies)
    company_options = [company['name'] for company in companies]
    company_name: str = click.prompt("select a company", type=click.Choice(company_options))
    return companies



if __name__ == "__main__":
    search_companies("muthoot")