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
def collect_multi_days_and_save(departure_airport, arrival_airport):
    today = datetime.today()
    schedules_all = {}

    for delta in range(1, 4):  # +1일 ~ +3일
        target_date = (today + timedelta(days=delta)).strftime("%Y%m%d")
        print(f"\n📅 {departure_airport}_{arrival_airport} 수집 중: {target_date}")  # 출발지, 도착지 정보 추가
        result = collect_flight_data(departure_airport, arrival_airport, target_date)
        schedules_all.update(result)
        print(f"✅ {departure_airport}_{arrival_airport} 수집 완료: {target_date} 가격 개수 : {len(result)} 누적 개수 : {len(schedules_all)}")

    # 수집 완료 후 파일 저장
    save_to_csv(schedules_all, departure_airport, arrival_airport)


def save_to_csv(schedules_dict, departure_airport, arrival_airport, output_dir="./output"):
    os.makedirs(output_dir, exist_ok=True)

    # 항공편 정보와 가격 정보를 따로 저장할 리스트
    flight_rows = []
    price_rows = []

    for info in schedules_dict.values():
        # FLIGHT_INFO_ID를 날짜-노선-편명 형식으로 생성
        flight_info_id = f"{info.get('departure_date')}{info.get('dep_airport')}{info.get('arr_airport')}{info.get('flight_code')}"

        # 항공편 정보 저장
        flight_rows.append({
            "ID": flight_info_id,  # 유니크한 ID로 생성된 flight_info_id 사용
            "DEPARTURE_DTM": info.get("dep_time"),  # 출발 시각
            "ARRIVAL_DTM": info.get("arr_time"),    # 도착 시각
            "CODE": info.get("flight_code"),        # 항공편 코드 (예: LJ881)
            "ROUTE_ID": "1",                        # 하드코딩된 값 (예시), 실제로는 외부 데이터를 사용해야 할 수도 있습니다.
            "AIRLINE_ID": "1",                      # 하드코딩된 값 (예시), 실제로는 외부 데이터를 사용해야 할 수도 있습니다.
            "CREATE_AT": pd.Timestamp.now(),       # 생성일
            "UPDATE_AT": pd.Timestamp.now(),       # 수정일
            "DELETE_AT": None,                     # 삭제일 (현재는 None)
            "DELETE_YN": "N"                       # 삭제 여부 (현재는 'N')
        })

        # 가격 정보가 있는 경우에만 가격 정보를 저장
        if "total_price" in info:
            price_rows.append({
                "SEARCH_DATE": info.get("search_date"),    # 검색일
                "PRICE": info["total_price"],              # 가격
                "FLIGHT_INFO_ID": flight_info_id,  # 생성된 유니크한 FLIGHT_INFO_ID
                "CREATE_AT": pd.Timestamp.now(),          # 생성일
                "UPDATE_AT": pd.Timestamp.now(),          # 수정일
                "DELETE_AT": None,                        # 삭제일 (현재는 None)
                "DELETE_YN": "N"                          # 삭제 여부 (현재는 'N')
            })

    # CSV 파일로 저장
    flight_info_df = pd.DataFrame(flight_rows)
    price_info_df = pd.DataFrame(price_rows)

    # 파일 저장 경로에서 CSV로 내보내기
    flight_info_df.to_csv(f"{output_dir}/flight_info_{departure_airport}_{arrival_airport}.csv", index=False, encoding="utf-8-sig")
    price_info_df.to_csv(f"{output_dir}/price_{departure_airport}_{arrival_airport}.csv", index=False, encoding="utf-8-sig")

    # 수집 완료 로그 출력
    print(f"✅ {departure_airport}_{arrival_airport} CSV 저장 완료!")
    print(f"  - 항공편 개수: {len(flight_info_df)}")
    print(f"  - 가격 개수: {len(price_info_df)}")


# 🏁 실행
if __name__ == "__main__":
    # 출발지와 도착지의 조합 리스트 (예: ICN-DAD, DAD-ICN)
    airport_pairs = [
        ("ICN", "DAD"),
        ("DAD", "ICN")
    ]

    # 각 공항 쌍에 대해 수집 함수 실행
    for departure_airport, arrival_airport in airport_pairs:
        collect_multi_days_and_save(departure_airport, arrival_airport)