import requests
import json
import time
import os

# ===== 설정 =====
url = "https://airline-api.naver.com/graphql"

headers = {
    "authority": "airline-api.naver.com",
    "method": "POST",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "cookie": "NNB=PDSIAZCILQRGM; NaverSuggestUse=use%26unuse; NFS=2; ASID=dc4bd1c30000018f2a405bf900000060; _ga=GA1.1.1698605432.1714476879; naverfinancial_CID=9c0efa0bd0164334cc03df060a7922c9; tooltipDisplayed=true; nstore_session=zxAqOFTImGK85zPh94c0XFdX; _tt_enable_cookie=1; ba.uuid=3878636e-80c6-4c4a-b65d-b12ac48f28ee; _ga_451MFZ9CFM=GS1.1.1735175188.2.0.1735175189.0.0.0; NID_AUT=mzocwZRWepMM7KP1V/JBsuwz8vBzi7lDfEzDyQalmt7JcQv/ZMQ0nK5DOQjjQPNw; NID_JKL=0KA1Ldp5m8znQ0FbxSl3yDowuz2Oe8AVj/DUmDmLMC8=; NAC=Sy3ZBggaMgPR; nstore_pagesession=i8dSKwqQennVQlsMVyl-322446; m_loc=a03a7f635277b1f1c0b352e714e1c8074b4e2efbe06f33c764f4fdfc739d07f2; _gcl_au=1.1.759143278.1741495256; _ttp=_c0IpwM0qFWOT3r_Yu8ZqvVyZSR.tt.1; _ga_9JHCQLWL5X=GS1.1.1741495255.1.0.1741495475.0.0.0; _ga_Q7G1QTKPGB=GS1.1.1741495255.5.0.1741495475.0.0.0; _ga_NFRXYYY5S0=GS1.1.1741495255.1.0.1741495475.0.0.0; NV_WETR_LAST_ACCESS_RGN_M=\"MDQxNzAzNDA=\"; NV_WETR_LOCATION_RGN_M=\"MDQxNzAzNDA=\"; NID_SES=AAABqudohrIAxy7N9D+iyiU+KsFxh5oPQik3RbjlmM9Z4aKcF7FbP04eY3hXcR4dQDomoH2YyU2opt2qLTaos100BaX1Xu4tjAQEljKrSpFeRdw7HTAQ/6pDzIxX09tSp4Dwcuy/ZNkZFzm0WvKLkxqZ/Wufo9HYFfILEhWrzkO0mSe/1r76lKgt+AO4vFy+PW7uFxq4NUBpWih5DbGnqeHQfAmnFp/KqUspAR4Lv9LhLrR8pZwpHRAq5GrQfuSiYiQ6LbX5hogfirnITEyc56iJek/W/b0cWmQT0TF/y/hePmhA1d6ZXhT6lXb+lL0hH/oFihPhAocEvjBW/s0OIA1wP1bzhNtvzSAIIT3SWJDjuWaUsPZb7faLHdkbNfVVwP1OvtDDRlUX+wvbmgj/LR+R5AKKnUXJEGxm4E9ORKieqJmwgmdauOfB9Dz9056US90mBJeDfDToZFffhOZuYOI0D/oUcVnekJGy6GW5f35IAxmSD3I+YXXAUh9/S2Vb1DYzFKE4FuyT8YsPo1s5soCe/8CxtdD7MhYzZkzVjlNtOp8H0aB9fDZ7h73E7BA+YAeTBA==; SRT30=1743687440; SRT5=1743689400; MM_PF=SEARCH; _naver_usersession_=QD/t8VdFUuDPye+Sg4ZlIw==; page_uid=i+IU/sprfMCss4V3PA4ssssssDs-392195; BUC=LG0LVpXXVYbTSa42vhdqrqAjKjXXSh57F4qbdLHEdJA=",
    "origin": "https://flight.naver.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://flight.naver.com/flights/international/ICN-DAD-20251210?adult=1&isDirect=true&fareType=Y",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# 📦 GraphQL 쿼리
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
      # 필요한 경우 아래도 같이 요청 가능
      # airlines
      # fareTypes
    }
  }
}
"""

# ===== 초기 요청 payload =====
payload = {
    "operationName": "getInternationalList",
    "variables": {
        "trip": "OW",
        "itinerary": [{"departureAirport": "ICN", "arrivalAirport": "DAD", "departureDate": "20251210"}],
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

# ===== 수집 관련 변수 =====
max_requests = 5
total_res_cnt = 0
all_fares = {}
schedules_dict = {}

# ===== 요청 반복 =====
for i in range(1, max_requests + 1):
    print(f"\n📦 요청 {i}차 보내는 중...")

    print("▶ 요청에 사용한 값:")
    print(f"   galileoKey     : {payload['variables']['galileoKey']}")
    print(f"   galileoFlag    : {payload['variables']['galileoFlag']}")
    print(f"   travelBizKey   : {payload['variables']['travelBizKey']}")
    print(f"   travelBizFlag  : {payload['variables']['travelBizFlag']}")

    res = requests.post(url, headers=headers, data=json.dumps(payload))
    data = res.json()["data"]["internationalList"]

    # 키 갱신
    payload["variables"]["galileoKey"] = data["galileoKey"]
    payload["variables"]["travelBizKey"] = data["travelBizKey"]
    payload["variables"]["galileoFlag"] = data["galileoFlag"]
    payload["variables"]["travelBizFlag"] = data["travelBizFlag"]

    res_cnt = data["resCnt"]
    total_cnt = data["totalResCnt"]
    total_res_cnt += res_cnt

    print(f"✅ 응답에서 받은 값:")
    print(f"   galileoKey     : {data['galileoKey']}")
    print(f"   galileoFlag    : {data['galileoFlag']}")
    print(f"   travelBizKey   : {data['travelBizKey']}")
    print(f"   travelBizFlag  : {data['travelBizFlag']}")
    print(f"🔹 이번 요청에서 받은 결과 수: {res_cnt}개")
    print(f"🔹 전체 결과 개수 (totalResCnt): {total_cnt}개")
    print(f"📈 누적 수집된 결과 수: {total_res_cnt}개")

    # 결과에서 필요한 필드
    results = data.get("results", {})
    fares = results.get("fares", {})
    schedules = results.get("schedules", [])
    airlines = results.get("airlines", {})
    airports = results.get("airports", {})

    # ✈ 스케줄 누적
    schedules = results.get("schedules", [])
    if schedules:
        for schedule_map in schedules:
            for schedule_id, info in schedule_map.items():
                if schedule_id not in schedules_dict:
                    # 새로 등록
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
                    }

                # ✨ 출현 차수만 누적
                schedules_dict[schedule_id].setdefault("appeared_in", []).append(i)

    # 💰 가격 정보 처리
    fares = results.get("fares", {})
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
            })

            # ✅ 가격이 없거나, 지금 가격이 더 저렴한 경우만 갱신
            current_price = schedules_dict[flight_id].get("total_price")
            if current_price is None or total_price < current_price:
                schedules_dict[flight_id].update({
                    "fare": fare,
                    "tax": tax,
                    "qcharge": qcharge,
                    "total_price": total_price,
                })

        # ✅ 출현 차수 누적
        schedules_dict[flight_id].setdefault("appeared_in", []).append(i)

    # ✨ 누적된 가격 정보 종합 출력
    print(f"\n💰 가격 + 요청 정보 (요청 {i}차 기준):")

    # ✅ total_price 있는 항공편만 정렬
    sorted_items = sorted(
        [(fid, info) for fid, info in schedules_dict.items() if "total_price" in info],
        key=lambda x: x[1]["total_price"]
    )

    for idx, (flight_id, info) in enumerate(schedules_dict.items(), 1):
        total_price = info.get("total_price")
        fare = info.get("fare", 0)
        tax = info.get("tax", 0)
        qcharge = info.get("qcharge", 0)
        appeared = sorted(set(info.get("appeared_in", [])))

        if total_price:
            print(f"{idx}. {flight_id} ➤ 총 {total_price}원 (운임: {fare} / 세금: {tax} / 유류: {qcharge}) | 출현 차수: {appeared}")
        else:
            print(f"{idx}. {flight_id} ➤ ❌ 가격 정보 없음 | 출현 차수: {appeared}")

    time.sleep(2)


