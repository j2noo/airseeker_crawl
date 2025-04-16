import sys
import requests
import json
import time
import os
from datetime import datetime, timedelta
import pandas as pd

global route_id, date_suffix

# ✈️ 항공권 데이터 수집 함수
def collect_flight_data(departure_airport, arrival_airport, departure_date, max_requests=3):
    url = "https://airline-api.naver.com/graphql"

    headers = {
        "referer": f"https://flight.naver.com/flights/international/{departure_airport}-{arrival_airport}-{departure_date}?adult=1&isDirect=true&fareType=Y",
        "origin": "https://flight.naver.com",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
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
          airlines
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
    airline_dict = {}

    for i in range(1, max_requests + 1):
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        if res.status_code != 200:
            print(f"❌ 요청 실패! status={res.status_code}")
            print("응답 내용:", res.text)
            continue  # 또는 return {}, {}
        data = res.json()["data"]["internationalList"]

        # 키 갱신
        payload["variables"]["galileoKey"] = data["galileoKey"]
        payload["variables"]["travelBizKey"] = data["travelBizKey"]
        payload["variables"]["galileoFlag"] = data["galileoFlag"]
        payload["variables"]["travelBizFlag"] = data["travelBizFlag"]

        results = data.get("results", {})
        fares = results.get("fares", {})
        schedules = results.get("schedules", [])
        airlines = results.get("airlines", {})

        airline_dict.update(airlines)

        if schedules:
            for schedule_map in schedules:
                for schedule_id, info  in schedule_map.items():
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
                            "airline_code": airline_code,
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
                    "airline_code": "??",
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

    return schedules_dict, airline_dict


def is_korean_airline(code):
    korean_airlines = {'KE', 'OZ', '7C', 'LJ', 'BX', 'RS', 'TW', 'GW', '8L', 'HJ', '8B', 'AK', 'KAC', 'ZE'}
    return code in korean_airlines


def collect_multi_days_and_save(departure_airport, arrival_airport):
    today = datetime.today()
    schedules_all = {}
    airlines_all = {}

    for delta in range(1, 101):
        target_date = (today + timedelta(days=delta)).strftime("%Y%m%d")
        print(f"\n📅 {departure_airport}_{arrival_airport} 수집 중: {target_date}")
        schedules, airlines = collect_flight_data(departure_airport, arrival_airport, target_date)
        schedules_all.update(schedules)
        airlines_all.update(airlines)

    save_to_csv(schedules_all, departure_airport, arrival_airport, airlines_all)


def save_to_csv(schedules_dict, departure_airport, arrival_airport, airline_dict, output_dir="./output"):
    global route_id, date_suffix
    os.makedirs(output_dir, exist_ok=True)

    flight_rows = []
    price_rows = []

    for info in schedules_dict.values():
        flight_info_id = f"{info.get('departure_date')}{info.get('dep_airport')}{info.get('arr_airport')}{info.get('flight_code')}"
        airline_code = info.get("airline_code", "??")

        flight_rows.append({
            "ID": flight_info_id,
            "DEPARTURE_DTM": info.get("dep_time"),
            "ARRIVAL_DTM": info.get("arr_time"),
            "CODE": info.get("flight_code"),
            "ROUTE_ID": route_id,
            "AIRLINE_ID": airline_code,  # 매핑할 키
            "CREATE_AT": pd.Timestamp.now(),
            "UPDATE_AT": pd.Timestamp.now(),
            "DELETE_AT": None,
            "DELETE_YN": "N"
        })

        if "total_price" in info:
            price_rows.append({
                "SEARCH_DATE": info.get("search_date"),
                "PRICE": info["total_price"],
                "FLIGHT_INFO_ID": flight_info_id,
                "CREATE_AT": pd.Timestamp.now(),
                "UPDATE_AT": pd.Timestamp.now(),
                "DELETE_AT": None,
                "DELETE_YN": "N"
            })

    airline_rows = []
    for code, name in airline_dict.items():
        korean_yn = 'Y' if is_korean_airline(code) else 'N'
        airline_rows.append({
            "CODE": code,
            "NAME": name,
            "KOREAN_YN": korean_yn,
            "CREATE_AT": pd.Timestamp.now(),
            "UPDATE_AT": pd.Timestamp.now(),
            "DELETE_AT": None,
            "DELETE_YN": "N"
        })

    pd.DataFrame(flight_rows).to_csv(f"{output_dir}/flight_info_{departure_airport}_{arrival_airport}_{date_suffix}.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(price_rows).to_csv(f"{output_dir}/price_{departure_airport}_{arrival_airport}_{date_suffix}.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(airline_rows).drop_duplicates(subset=["CODE"]).to_csv(f"{output_dir}/airline.csv", index=False, encoding="utf-8-sig")

    print(f"✅ 모든 CSV 저장 완료! (항공편: {len(flight_rows)} / 가격: {len(price_rows)} / 항공사: {len(airline_rows)})")


if __name__ == "__main__":
    global route_id, date_suffix
    if len(sys.argv) != 5:
        print("Usage: python crawler.py <departure_airport> <arrival_airport> <route_id> <date_suffix>")
        sys.exit(1)

    departure_airport = sys.argv[1]
    arrival_airport = sys.argv[2]
    route_id = sys.argv[3]
    date_suffix = sys.argv[4]

    collect_multi_days_and_save(departure_airport, arrival_airport)
