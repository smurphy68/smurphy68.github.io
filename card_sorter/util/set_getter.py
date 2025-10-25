import json
import requests


def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            print(
                f"Error: Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def write_data_to_json_file(data, set_code):
    fp = f"json_sets/{set_code.upper()}.json"
    try:
        with open(fp, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Data has been written to {set_code.capitalize()}.json")
        json_file.close()
    except Exception as e:
        print(f"Error writing to {set_code.capitalize()}.json: {str(e)}")


def get_full_set(set_code):
    url = f'https://api.scryfall.com/cards/search?q=set%3A{set_code}+f%3Acommander'
    json_data = make_request(url)
    has_more = json_data["has_more"]
    data = json_data["data"]
    while has_more:
        next_page = json_data["next_page"]
        json_data = make_request(next_page)
        data += json_data["data"]
        has_more = json_data["has_more"]
    write_data_to_json_file(data, set_code)
