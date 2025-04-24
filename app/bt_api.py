import os
import time
import hashlib
import requests
from typing import List, Optional, Dict, Any


# Tắt warning SSL self-signed
requests.packages.urllib3.disable_warnings()

class BtApi:
    def __init__(self, bt_panel: str, bt_key: str):
        self.bt_panel = bt_panel.rstrip('/')
        self.bt_key = bt_key
        # session hoặc agent nếu cần
        self.session = requests.Session()
        self.session.verify = False

    def _get_signed_data(self) -> Dict[str, Any]:
        now = int(time.time())
        md5_key = hashlib.md5(self.bt_key.encode()).hexdigest()
        token = hashlib.md5(f"{now}{md5_key}".encode()).hexdigest()
        return {'request_time': now, 'request_token': token}
    
    def call_api(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gọi API POST lên endpoint: {bt_panel}{path}, tham số form-urlencode
        """
        url = f"{self.bt_panel}{path}"
        # gộp ký và params
        data = {**self._get_signed_data(), **params}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-http-token': self.bt_key
        }
        resp = self.session.post(url, data=data, headers=headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_sites(self, page: int = 1, limit: int = 50,
                  search: str = '', order: str = '', type_: int = -1) -> List[Dict[str, Any]]:
        res = self.call_api("/data?action=getData", {
            'table': 'sites',
            'p': page,
            'limit': limit,
            'search': search,
            'order': order,
            'type': type_
        })
        return res.get('data', [])


