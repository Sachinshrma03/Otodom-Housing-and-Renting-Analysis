import requests
import csv
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(url, headers, payload, retries=3):
    for _ in range(retries):
        logger.info(f"Attempting request to URL: {url}")
        try:
            response = requests.get(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            time.sleep(5)  # Adjust the delay as needed
            continue

        if response.status_code == 200:
            logger.info("Request successful. Processing response...")
            return response.json()
        elif response.status_code == 403:
            logger.warning(f"Failed to retrieve data. Status code: {response.status_code}. Retrying...")
            time.sleep(5)  # Adjust the delay as needed
        else:
            logger.error(f"Failed to retrieve data. Status code: {response.status_code}. Giving up.")
            return None

    return None

def extract_data(item):
    # Extract data from the item and return a dictionary
    property_id = item.get('id', '')
    title = item.get('title', '')
    estate = item.get('estate', '')
    transaction = item.get('transaction', '')

    location = item.get('location', {})
    city = location['address']['city']['name'] if 'address' in location and 'city' in location['address'] else ''
    province = location['address']['province']['name'] if 'address' in location and 'province' in location['address'] else ''

    reverse_geocoding = location.get('reverseGeocoding', {})
    locations = reverse_geocoding['locations'][-1]['fullName'] if 'locations' in reverse_geocoding and reverse_geocoding['locations'] else ''

    is_private_owner = item.get('isPrivateOwner', '')
    agency_name = item['agency']['name'] if 'agency' in item and item['agency'] and 'name' in item['agency'] else ''
    total_price = f"{item['totalPrice']['value']} {item['totalPrice']['currency']}" if 'totalPrice' in item and item['totalPrice'] else ''
    rent_price = f"{item['rentPrice']['value']} {item['rentPrice']['currency']}" if 'rentPrice' in item and item['rentPrice'] and 'value' in item['rentPrice'] else ''
    area_in_square_meters = item.get('areaInSquareMeters', '')
    rooms_number = item.get('roomsNumber', '')
    date_created = item.get('dateCreated', '')
    description = item['seo']['details']['description'] if 'seo' in item and 'details' in item['seo'] else ''

    return {
        'id': property_id,
        'title': title,
        'estate': estate,
        'transaction': transaction,
        'city': city,
        'province': province,
        'locations': locations,
        'isPrivateOwner': is_private_owner,
        'agency': agency_name,
        'totalPrice': total_price,
        'rentPrice': rent_price,
        'areaInSquareMeters': area_in_square_meters,
        'roomsNumber': rooms_number,
        'dateCreated': date_created,
        'description': description,
    }


def save_to_csv(data, file_path):
    if data:
        csv_columns = data[0].keys()

        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        logger.info(f"Data has been successfully extracted and saved to '{file_path}'.")
    else:
        logger.warning("No data was extracted.")

def main():
    # Configuration
    url_template = "https://www.otodom.pl/_next/data/dTgdsGGEBfF8SgnEUFTli/pl/wyniki/{}/{}/cala-polska.json?viewType=listing&searchingCriteria={}&searchingCriteria={}&searchingCriteria=cala-polska&page={}"
    payload = {}
    headers = {
  'authority': 'www.otodom.pl',
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'baggage': 'sentry-environment=otodompl-prd,sentry-release=frontend-platform%40local_build-otodompl,sentry-public_key=6c4675ab868d06ef702e62aaf3fd60fd,sentry-trace_id=94a5f82495774c159d680170902ef642,sentry-sample_rate=0,sentry-transaction=%2Fpl%2Fwyniki%2F%5B%5B...searchingCriteria%5D%5D,sentry-sampled=false',
  'cookie': 'lang=pl; laquesis=euads-4691^@b^#remd-1201^@a^#see-1660^@c^#see-1827^@a^#see-1957^@b^#sfs-540^@b^#sfs-725^@b^#sfs-887^@b^#smr-2130^@b; laquesisff=gre-12226^#rer-165^#rer-166^#rst-73^#rst-74; lqstatus=1701196270; dfp_user_id=e1d36efa-8c67-4a2d-8239-f114bc112d80; OptanonAlertBoxClosed=2023-11-28T18:10:58.038Z; eupubconsent-v2=CP18MGQP18MGQAcABBENDgCgAAAAAH_AAAYgg1Nf_X__b2_r8_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuyJGQm2jCKBACIKwkKoFABRAJC0QGELq4KdhcBPrCRACBFAA8EAIYAUZAAgAAEgCQiACQI4EAgEAgEAAIAFQgEADGwADwAtBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KBBKD9QVwgDLLAig0f8VCAhWQMVgRCQsXocASAl4kkD3VG-AAhACgFFKFYik_MAQ4Jmy1V4om0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.YAAAD_gAAAAA; _hjSessionUser_3074646=eyJpZCI6IjA5MjUwYjViLWE0ODMtNWE3ZS04NWIxLWYzZTYwZjk5OWMzYyIsImNyZWF0ZWQiOjE3MDE1MzAxMzg2NzIsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample_3074646=0; _hjSession_3074646=eyJpZCI6IjM2OWU4MDRjLTVhMDUtNGYyOC1iMmI4LTBlYWU2MmMwOTg0YiIsImNyZWF0ZWQiOjE3MDE1MzAxMzg2NzUsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Dec+02+2023+20%3A46%3A00+GMT%2B0530+(India+Standard+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=42e6b12d-3e87-4c40-acbf-fbe52919739d&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2Cgad%3A0%2CSTACK42%3A0&AwaitingReconsent=false&geolocation=IN%3BDL',
  'referer': 'https://www.otodom.pl/',
  'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sentry-trace': '94a5f82495774c159d680170902ef642-97da730de2a86983-0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
  'x-nextjs-data': '1'
}
    csv_file_path = 'otodom_data.csv'

    # Extracted data
    extracted_data = []

    for search_type in ['sprzedaz', 'wynajem']:
        for property_type in ['mieszkanie', 'kawalerka', 'dom', 'dzialka']:
            for page_number in range(1, 51):  # Adjust the range based on the number of pages you want
                url = url_template.format(search_type, property_type, search_type, property_type, page_number)
                logger.info(f"Processing this URL: {url}")

                # Get data for the current page
                data = make_request(url, headers, payload)

                if data is not None and 'pageProps' in data:
                    items = data['pageProps']['data']['searchAds']['items']
                    logger.info(items)

                    if items and isinstance(items, list):
                        for item in items:
                            # Extract data from the item
                            extracted_data.append(extract_data(item))

                        logger.info("Data Extraction complete for this page")
                    else:
                        logger.warning("No items found for this page")
                else:
                    logger.warning("Failed to retrieve data for this page.")

    # Save the extracted data to a CSV file
    save_to_csv(extracted_data, csv_file_path)

if __name__ == "__main__":
    main()
