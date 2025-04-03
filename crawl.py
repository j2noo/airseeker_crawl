import requests
import json
import time

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
    "referer": "https://flight.naver.com/flights/international/ICN-DAD-20250605?adult=1&isDirect=true&fareType=Y",
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
      carbonEmissionAverage {
        directFlightCarbonEmissionItineraryAverage
        directFlightCarbonEmissionAverage
      }
    }
  }
}
"""

# 🥇 1차 요청용 payload
payload = {
    "operationName": "getInternationalList",
    "variables": {
        "trip": "OW",
        "itinerary": [{
            "departureAirport": "ICN",
            "arrivalAirport": "DAD",
            "departureDate": "20250605"
        }],
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

# ===== 초기 요청 payload =====
payload = {
    "operationName": "getInternationalList",
    "variables": {
        "trip": "OW",
        "itinerary": [{"departureAirport": "ICN", "arrivalAirport": "DAD", "departureDate": "20250605"}],
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

# ===== 요청 반복 =====
for i in range(1, max_requests + 1):
    print(f"\n📦 요청 {i}차 보내는 중...")

    # 요청 시 사용한 키/flag 값
    print("▶ 요청에 사용한 값:")
    print(f"   galileoKey     : {payload['variables']['galileoKey']}")
    print(f"   galileoFlag    : {payload['variables']['galileoFlag']}")
    print(f"   travelBizKey   : {payload['variables']['travelBizKey']}")
    print(f"   travelBizFlag  : {payload['variables']['travelBizFlag']}")

    # 요청 전송
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    data = res.json()["data"]["internationalList"]

    # 응답에서 받은 키/flag
    print("✅ 응답에서 받은 값:")
    print(f"   galileoKey     : {data['galileoKey']}")
    print(f"   galileoFlag    : {data['galileoFlag']}")
    print(f"   travelBizKey   : {data['travelBizKey']}")
    print(f"   travelBizFlag  : {data['travelBizFlag']}")

    # 키 업데이트
    payload["variables"]["galileoKey"] = data["galileoKey"]
    payload["variables"]["travelBizKey"] = data["travelBizKey"]
    payload["variables"]["galileoFlag"] = data["galileoFlag"]
    payload["variables"]["travelBizFlag"] = data["travelBizFlag"]

    # 수집 카운트 출력
    res_cnt = data["resCnt"]
    total_cnt = data["totalResCnt"]
    total_res_cnt += res_cnt

    print(f"🔹 이번 요청에서 받은 결과 수: {res_cnt}개")
    print(f"🔹 전체 결과 개수 (totalResCnt): {total_cnt}개")
    print(f"📈 누적 수집된 결과 수: {total_res_cnt}개")

    # 가격 출력
    fares = data["results"].get("fares", {})
    print("💰 가격 정보:")
    for flight_id, fare_info in fares.items():
        fare_list = fare_info.get("A01", [])
        if not fare_list:
            continue
        adult_info = fare_list[0].get("Adult", {})
        price = adult_info.get("NaverFare", adult_info.get("Fare", "N/A"))
        all_fares[flight_id] = price
        print(f"   - {flight_id} ➤ {price} 원")

    time.sleep(2)
