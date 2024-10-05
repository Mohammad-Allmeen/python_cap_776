import requests

class Geo:
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"

    def get_geolocation(self, ip_address):
        try:
            response = requests.get(f"{self.api_url}{ip_address}")
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'fail':
                    print(f"Error: {data['message']}")
                    return None
                return data
            else:
                print("Error: Unable to connect to the geolocation service.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None

    def run(self):
        ip = input("Enter IP address (or press Enter for your own IP): ")
        if not ip:
            ip = requests.get('https://api.ipify.org').text  # Getting the user's public IP

        location_data = self.get_geolocation(ip)
        if location_data:
            print(f"Country: {location_data['country']}")
            print(f"City: {location_data['city']}")
            print(f"Region: {location_data['regionName']}")
            print(f"Latitude: {location_data['lat']}")
            print(f"Longitude: {location_data['lon']}")
            print(f"Timezone: {location_data['timezone']}")
            print(f"ISP: {location_data['isp']}")
