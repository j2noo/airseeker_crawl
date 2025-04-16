import subprocess
from datetime import datetime


def run_crawler(departure_airport, arrival_airport, route_id, date_suffix):
    try:
        current_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        print(f"1️⃣ {departure_airport}_{arrival_airport} 크롤러 실행 요청 at {current_time}")
        # 크롤링 후, 생성된 파일명(date_suffix)을 전달하며 실행
        subprocess.run(['python', 'crawler.py', departure_airport, arrival_airport, route_id, date_suffix], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running crawler: {e}")


def run_insert_flight(file_name):
    try:
        print(f"2️⃣ {departure_airport}_{arrival_airport} FLIGHT_INFO DB Inserter 실행 요청")
        subprocess.run(['python', 'inserter_flight_info.py', file_name], check=True)  # 파일명 전달
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running insert_flight: {e}")


def run_insert_price(file_name):
    try:
        print(f"3️⃣ {departure_airport}_{arrival_airport} PRICE DB Inserter 실행 요청")
        subprocess.run(['python', 'inserter_price.py', file_name], check=True)  # 파일명 전달
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running insert_price: {e}")


if __name__ == "__main__":
    airport_pairs = [
        ("ICN", "DAD", "1"),
        ("DAD", "ICN", "2")
    ]

    # 현재 날짜를 파일명에 포함시키기 위한 접미사 생성
    date_suffix = datetime.today().strftime("%Y%m%d")

    for departure_airport, arrival_airport, route_id in airport_pairs:
        # 크롤러 실행
        run_crawler(departure_airport, arrival_airport, route_id, date_suffix)

        # 파일명 설정
        flight_file = f"output/flight_info_{departure_airport}_{arrival_airport}_{date_suffix}.csv"
        price_file = f"output/price_{departure_airport}_{arrival_airport}_{date_suffix}.csv"

        # 항공편 데이터 삽입
        run_insert_flight(flight_file)

        # 가격 데이터 삽입
        run_insert_price(price_file)
