import requests

class Cloudflare:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        
    def get_zone_id(self, domain):
        url = f"{self.base_url}/zones"
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }
        
        params = {
            'name': domain  # Tên miền bạn muốn lấy zone_id
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            zones = response.json().get("result", [])
            if zones:
                zone_id = zones[0]["id"]  # Lấy zone_id của trang web
                print(f"Zone ID: {zone_id}")
                return zone_id
            else:
                print("Không tìm thấy zone_id cho trang web này.")
                return None
        else:
            print("Lỗi khi lấy zone_id:", response.json())
            return None

    def enable_under_attack_mode(self, zone_id):
        url = f"{self.base_url}/zones/{zone_id}/settings/security_level"
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }
        
        data = {
            "value": "under_attack"  # Bật Under Attack Mode (Captcha)
        }
        
        response = requests.patch(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Chế độ Under Attack (Captcha) đã được bật trên Cloudflare.")
            return response.json()
        else:
            print("Lỗi khi bật Under Attack Mode trên Cloudflare:", response.json())
            return None

    def disable_under_attack_mode(self, zone_id):
        url = f"{self.base_url}/zones/{zone_id}/settings/security_level"  # Sửa lại đây để dùng zone_id
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }
        data = {
            "value": "high"  # Thay bằng mức bảo mật thấp hơn khi tắt Under Attack Mode
        }
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code == 200:
            return f"✅ WAF captcha tắt cho {zone_id}"
        else:
            return f"❌ Tắt WAF thất bại cho {zone_id}: {response.json()}"


