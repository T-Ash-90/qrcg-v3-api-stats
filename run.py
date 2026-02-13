import requests
import csv
import time
from datetime import datetime

BASE_URL = "https://api.qrcg.com/v3"
RATE_LIMIT_DELAY = 0.12  # respect 10 requests/sec


def get_all_qr_codes(api_key):
    qr_codes = []
    cursor = None 
    page_count = 0
    max_pages = 10000

    headers = {
        "Authorization": f"Key {api_key}",
        "Accept": "application/json"
    }

    while True:
        if cursor:
            url = f"{BASE_URL}/qrcodes?perPage=50&cursor={cursor}"
        else:
            url = f"{BASE_URL}/qrcodes?perPage=50"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        qr_codes.extend(data.get("data", []))

        pagination = data.get("pagination", {})
        has_more = pagination.get("hasMore", False)
        next_cursor = pagination.get("nextCursor")

        page_count += 1

        print(f"Fetched page {page_count} | Total codes so far: {len(qr_codes)}")

        if has_more and next_cursor:
            cursor = next_cursor
            time.sleep(RATE_LIMIT_DELAY)
        else:
            break

        if page_count >= max_pages:
            print("Pagination safeguard triggered.")
            break

    return qr_codes


def get_total_scans(api_key, qr_id):
    headers = {
        "Authorization": f"Key {api_key}",
        "Accept": "application/json"
    }

    url = f"{BASE_URL}/qrcodes/{qr_id}/scans/total"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    time.sleep(RATE_LIMIT_DELAY)
    return response.json()


def get_range_scans(api_key, qr_id, start_date, end_date):
    headers = {
        "Authorization": f"Key {api_key}",
        "Accept": "application/json"
    }

    url = (
        f"{BASE_URL}/qrcodes/{qr_id}/scans/totals"
        f"?startDate={start_date}&endDate={end_date}&interval=day"
    )

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    time.sleep(RATE_LIMIT_DELAY)
    return response.json()


def main():
    print("\nQR Code Generator Statistics Export Tool\n")

    api_key = input("Enter your API Key: ").strip()

    print("\nChoose statistics type:")
    print("1 - All-time totals")
    print("2 - Between a date range")

    choice = input("Enter 1 or 2: ").strip()

    start_date = None
    end_date = None

    if choice == "2":
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return

    print("\nFetching QR Codes...")
    qr_codes = get_all_qr_codes(api_key)
    print(f"\nFound {len(qr_codes)} QR Codes.\n")

    filename = "qr_code_statistics.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if choice == "1":
            writer.writerow([
                "QR ID", "Title", "Type", "Status",
                "Created At", "Total Scans", "Unique Scans"
            ])
        else:
            writer.writerow([
                "QR ID", "Title", "Type", "Status",
                "Created At", "Date", "Total Scans", "Unique Scans"
            ])

        for index, qr in enumerate(qr_codes, start=1):
            qr_id = qr["id"]
            print(f"Processing {index}/{len(qr_codes)} - QR ID: {qr_id}")

            if choice == "1":
                stats = get_total_scans(api_key, qr_id)

                writer.writerow([
                    qr_id,
                    qr.get("title"),
                    qr.get("type"),
                    qr.get("status"),
                    qr.get("createdAt"),
                    stats.get("total"),
                    stats.get("unique")
                ])

            else:
                stats = get_range_scans(api_key, qr_id, start_date, end_date)

                for entry in stats.get("scans", []):
                    total = entry.get("total", 0)
                    unique = entry.get("unique", 0)

                    if total > 0 or unique > 0:
                        writer.writerow([
                            qr_id,
                            qr.get("title"),
                            qr.get("type"),
                            qr.get("status"),
                            qr.get("createdAt"),
                            entry.get("time"),
                            total,
                            unique
                        ])

    print(f"\nExport complete! Data saved to {filename}")


if __name__ == "__main__":
    main()