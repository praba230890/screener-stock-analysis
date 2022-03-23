from unittest.mock import patch, Mock

from screener_analysis.app import search_companies


class TestSearchCompanies:

    muthoot_search_response = [{'id': 2168, 'name': 'Muthoot Finance Ltd', 'url': '/company/MUTHOOTFIN/'}, {'id': 2167, 'name': 'Muthoot Capital Services Ltd', 'url': '/company/MUTHOOTCAP/'}]

    @patch('requests.get')
    def test_search_companies_positive(self, mocked_get):
        mocked_get.return_value = Mock(status_code=200, json=lambda : self.muthoot_search_response)
        assert search_companies("muthoot") == self.muthoot_search_response
    
    @patch('requests.get')
    def test_search_companies_negative(self, mocked_get):
        mocked_get.return_value = Mock(status_code=200, json=lambda : {"data": {"id": "test"}})
        assert search_companies("ven") != self.muthoot_search_response