screener_base: str = "https://www.screener.in"

company_search_url: str = f"{screener_base}/api/company/search/?q="

quick_ratios_url: str = screener_base+"/api/company/{}/quick_ratios/"

dataset_url: str = screener_base+"/api/company/{}/chart/?q=Price-DMA50-DMA200-Volume&days=365"