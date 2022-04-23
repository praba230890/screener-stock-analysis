from typing import List
import requests

import click
import lxml.html

from config.api import company_search_url, screener_base, dataset_url

def get_dataset(company_id: str) -> List[dict]:
    """
    Get the data set for a company.
    """
    url = dataset_url.format(company_id)
    data_set = requests.get(url).json()
    return data_set

def get_fundamentals(company) -> List[dict]:
    """
    Get fundamentals for a list of companies.
    """
    url = screener_base + company["url"]
    company_page = requests.get(url)
    root = lxml.html.fromstring(company_page.text)
    # ind = 0
    # quarterly_pl = []
    # yearly_pl = []
    # balance_sheet = []
    # cashflows = []
    # ratios_table = []
    # shareholding = []
    # for tbl in root.xpath('//table'):
    #     if ind == 0:
    #         quarterly_pl = tbl.xpath('.//tr/td//text()')
    #     elif ind == 1:
    #         yearly_pl = tbl.xpath('.//tr/td//text()')
    #     elif ind == 2:
    #         balance_sheet = tbl.xpath('.//tr/td//text()')
    #     elif ind == 3:
    #         cashflows = tbl.xpath('.//tr/td//text()')
    #     elif ind == 4:
    #         ratios_table = tbl.xpath('.//tr/td//text()')
    #     elif ind == 5:
    #         shareholding = tbl.xpath('.//tr/td//text()')
    #     ind += 1

    warehouse_id = root.xpath("/html/body/main/div[1]/@data-warehouse-id")[0]
    market_cap = root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[1]/span[2]/span/text()")[0]
    print(f"{warehouse_id} {market_cap}")
    fundamentals = {
        "company": company["name"],
        "market_cap": market_cap,
        "current_price": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[2]/span[2]/span/text()")[0],
        "high": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[3]/span[2]/span[1]/text()")[0],
        "low": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[3]/span[2]/span[2]/text()")[0],
        "P/E": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[4]/span[2]/span/text()")[0] if root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[4]/span[2]/span/text()") else "N/A",
        "Book Value": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[5]/span[2]/span/text()")[0],
        "Divident Yield": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[6]/span[2]/span/text()")[0] if root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[6]/span[2]/span/text()") else "N/A",
        "ROCE": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[7]/span[2]/span/text()")[0] if len(root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[7]/span[2]/span/text()")) > 0 else "N/A",
        "ROE": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[8]/span[2]/span/text()")[0] if len(root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[8]/span[2]/span/text()")) > 0 else "N/A",
        "Face Value": root.xpath("/html/body/main/div[2]/div[3]/div[2]/ul/li[9]/span[2]/span/text()")[0],
    }
    dataset = get_dataset(company["id"])
    return {
            "dataset": dataset,
            "fundamentals": fundamentals
        }

def search_companies() -> List[dict]:
    """
    Search for a company name in screener.
    """
    company_name: str = click.prompt("Please enter a company name", type=str)
    url: str = f"{company_search_url}{company_name}"
    companies = requests.get(url).json()
    print(companies)
    company_options = [company["name"] for company in companies]
    company_name: str = click.prompt("select a company", type=click.Choice(company_options))
    selected_company = [company for company in companies if company["name"] == company_name][0]
    print(selected_company, " company selected")
    fundamentals = get_fundamentals(selected_company)
    print(fundamentals, " fundamentals")
    return fundamentals



if __name__ == "__main__":
    search_companies()