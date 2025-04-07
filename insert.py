import requests
import json
import time
import os
from datetime import datetime, timedelta
import pandas as pd

# ✈️ 항공권 데이터 수집 함수
def collect_flight_data(departure_airport, arrival_airport, departure_date, max_requests=3):
    url = "https://airline-api.naver.com/graphql"

    headers = {
        "referer": f"https://flight.naver.com/flights/international/{departure_airport}-{arrival_airport}-{departure_date}?adult=1&isDirect=true&fareType=Y",
        "origin": "https://flight.naver.com",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    query = """
    query getInternationalList($trip: InternationalList_TripType!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: InternationalList_CabinClass!, $where: InternationalList_DeviceType = pc, $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {
      internationalList(
        input: {
          trip: $trip,
          itinerary: $itinerary,
          person: {adult: $adult, child: $child, infant: $infant},
          fareType: $fareType,
          where: $where,
          isDirect: $isDirect,
          stayLength: $stayLength,
          galileoKey: $galileoKey,
          galileoFlag: $galileoFlag,
          travelBizKey: $travelBizKey,
          travelBizFlag: $travelBizFlag
        }
      ) {
        galileoKey
        galileoFlag
        travelBizKey
        travelBizFlag
        totalResCnt
        resCnt
        results {
          fares
          schedules
        }
      }
    }
    """

    payload = {
        "operationName": "getInternationalList",
        "variables": {
            "trip": "OW",
            "itinerary": [{"departureAirport": departure_airport, "arrivalAirport": arrival_airport, "departureDate": departure_date}],
            "adult": 1,
            "child": 0,
            "infant": 0,
            "fareType": "Y",
            "where": "pc",
            "isDirect": True,
            "stayLength": "",
            "galileoFlag": True,
            "galileoKey": "",
            "travelBizFlag": True,
            "travelBizKey": ""
        },
        "query": query
    }

    schedules_dict = {}

    for i in range(1, max_requests + 1):
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        data = res.json()["data"]["internationalList"]

        payload["variables"]["galileoKey"] = data["galileoKey"]
        payload["variables"]["travelBizKey"] = data["travelBizKey"]
        payload["variables"]["galileoFlag"] = data["galileoFlag"]
        payload["variables"]["travelBizFlag"] = data["travelBizFlag"]

        results = data.get("results", {})
        fares = results.get("fares", {})
        schedules = results.get("schedules", [])

        if schedules:
            for schedule_map in schedules:
                for schedule_id, info in schedule_map.items():
                    if schedule_id not in schedules_dict:
                        detail = info.get("detail", [{}])[0]
                        dep_airport = detail.get("sa", "??")
                        arr_airport = detail.get("ea", "??")
                        airline_code = detail.get("av", "??")
                        flight_num = detail.get("fn", "??")
                        sdt = detail.get("sdt", "")
                        edt = detail.get("edt", "")
                        journey_time = info.get("journeyTime", ["??", "??"])

                        dep_time = f"{sdt[:4]}-{sdt[4:6]}-{sdt[6:8]} {sdt[8:10]}:{sdt[10:]}" if len(sdt) == 12 else "--"
                        arr_time = f"{edt[:4]}-{edt[4:6]}-{edt[6:8]} {edt[8:10]}:{edt[10:]}" if len(edt) == 12 else "--"

                        schedules_dict[schedule_id] = {
                            "dep_airport": dep_airport,
                            "arr_airport": arr_airport,
                            "flight_code": f"{airline_code}{flight_num}",
                            "dep_time": dep_time,
                            "arr_time": arr_time,
                            "duration": f"{journey_time[0]}시간 {journey_time[1]}분",
                            "appeared_in": [],
                            "search_date": datetime.today().strftime("%Y-%m-%d"),
                            "departure_date": departure_date
                        }

                    schedules_dict[schedule_id].setdefault("appeared_in", []).append(i)

        for flight_id, fare_info in fares.items():
            fare_data = fare_info.get("fare", {})
            a01_fare_list = fare_data.get("A01", [])

            if a01_fare_list:
                adult = a01_fare_list[0].get("Adult", {})
                fare = int(adult.get("Fare", 0))
                tax = int(adult.get("Tax", 0))
                qcharge = int(adult.get("QCharge", 0))
                total_price = fare + tax + qcharge

                schedules_dict.setdefault(flight_id, {
                    "flight_code": "??",
                    "dep_airport": "??",
                    "arr_airport": "??",
                    "dep_time": "--",
                    "arr_time": "--",
                    "duration": "--",
                    "appeared_in": [],
                    "search_date": datetime.today().strftime("%Y-%m-%d"),
                    "departure_date": departure_date
                })

                current_price = schedules_dict[flight_id].get("total_price")
                if current_price is None or total_price < current_price:
                    schedules_dict[flight_id].update({
                        "fare": fare,
                        "tax": tax,
                        "qcharge": qcharge,
                        "total_price": total_price,
                    })

            schedules_dict[flight_id].setdefault("appeared_in", []).append(i)

        time.sleep(2)

    return schedules_dict


# ✨ 전체 수집 & 저장 로직
def collect_multi_days_and_save():
    today = datetime.today()
    schedules_all = {}

    for delta in range(1, 4):  # +1일 ~ +3일
        target_date = (today + timedelta(days=delta)).strftime("%Y%m%d")
        print(f"\n📅 수집 중: {target_date}")
        result = collect_flight_data("ICN", "DAD", target_date)
        schedules_all.update(result)

    # CSV로 저장
    save_to_csv(schedules_all)
    
def save_to_csv(schedules_dict, output_dir="./output"):
    os.makedirs(output_dir, exist_ok=True)

    # 항공편 정보와 가격 정보를 따로 저장할 리스트
    flight_rows = []
    price_rows = []

    for info in schedules_dict.values():
        # 항공편 정보 저장
        flight_rows.append({
            "ID": info.get("flight_code"),  # flight_code는 ID로 저장
            "DEPARTURE_DTM": info.get("dep_time"),
            "ARRIVAL_DTM": info.get("arr_time"),
            "DEP_AIRPORT_CODE": info.get("dep_airport"),
            "ARR_AIRPORT_CODE": info.get("arr_airport"),
            "ROUTE_ID": "1",  # 하드코딩된 값 (예시), 실제로는 외부 데이터를 사용해야 할 수도 있습니다.
            "AIRLINE_ID": "1"  # 하드코딩된 값 (예시), 실제로는 외부 데이터를 사용해야 할 수도 있습니다.
        })

        # 가격 정보가 있는 경우에만 가격 정보를 저장
        if "total_price" in info:
            price_rows.append({
                "ID": f"{info.get('flight_code')}_price",  # 유니크한 ID로 항공편 코드+_price
                "SEARCH_DATE": info.get("search_date"),
                "PRICE": info["total_price"],
                "flight_info_id": info.get("flight_code")  # flight_info_id는 flight_code와 연결
            })

    # CSV 파일로 저장
    flight_info_df = pd.DataFrame(flight_rows)
    price_info_df = pd.DataFrame(price_rows)

    flight_info_df.to_csv(f"{output_dir}/flight_info.csv", index=False, encoding="utf-8-sig")
    price_info_df.to_csv(f"{output_dir}/price_info.csv", index=False, encoding="utf-8-sig")

    print("✅ CSV 저장 완료!")

    
# 🏁 실행
if __name__ == "__main__":
    collect_multi_days_and_save()
