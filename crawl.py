import requests
import json

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
    "origin": "https://flight.naver.com",
    "pragma": "no-cache",
    "referer": "https://flight.naver.com/flights/international/ICN-OSA-20250605?adult=1&isDirect=true&fareType=Y",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "x-client-language": "ko",
    "cookie": 'NNB=PDSIAZCILQRGM; NaverSuggestUse=use%26unuse; NFS=2; ASID=dc4bd1c30000018f2a405bf900000060; _ga=GA1.1.1698605432.1714476879; naverfinancial_CID=9c0efa0bd0164334cc03df060a7922c9; tooltipDisplayed=true; nstore_session=zxAqOFTImGK85zPh94c0XFdX; _tt_enable_cookie=1; ba.uuid=3878636e-80c6-4c4a-b65d-b12ac48f28ee; _ga_451MFZ9CFM=GS1.1.1735175188.2.0.1735175189.0.0.0; NID_AUT=mzocwZRWepMM7KP1V/JBsuwz8vBzi7lDfEzDyQalmt7JcQv/ZMQ0nK5DOQjjQPNw; NID_JKL=0KA1Ldp5m8znQ0FbxSl3yDowuz2Oe8AVj/DUmDmLMC8=; NAC=Sy3ZBggaMgPR; nstore_pagesession=i8dSKwqQennVQlsMVyl-322446; m_loc=a03a7f635277b1f1c0b352e714e1c8074b4e2efbe06f33c764f4fdfc739d07f2; _gcl_au=1.1.759143278.1741495256; _ttp=_c0IpwM0qFWOT3r_Yu8ZqvVyZSR.tt.1; _ga_9JHCQLWL5X=GS1.1.1741495255.1.0.1741495475.0.0.0; _ga_Q7G1QTKPGB=GS1.1.1741495255.5.0.1741495475.0.0.0; _ga_NFRXYYY5S0=GS1.1.1741495255.1.0.1741495475.0.0.0; NV_WETR_LAST_ACCESS_RGN_M="MDQxNzAzNDA="; NV_WETR_LOCATION_RGN_M="MDQxNzAzNDA="; SRT30=1743165457; page_uid=i+jkOwqX5mNsssHlPGNsssssthV-255792; NID_SES=AAABrKj95sd9PF9ixu+BYtcO9YCydypu5w1mRG45osSYB6g70jv1s3LoJcBV3czFdVjD5nZ8CIdKQSWWAqogg2trknNj+X1kCL+P3WXhs67D9HWSeuT2Xu6C1UNSj6UiYTLcHimd7LYZ6bJiIK8irgWw5BE7RRlLqOVaoCmnMw7YP2RIIAZMPnBMBRgyf29WxhEC645PcY1FVbfdDzu9p7DPnz7Bih6V2Z+PBs1CKm65jXaeCKX52Q/fdgHoaeV/3TpMfV6BPV4tp6DOe6eU3vHiwYOQwva8jNfK5RPTCayIvvHUR5O1UnCxEy1TI0nARTstP5vwwVMq9QW18wjEcuar2Ar2B7yscYhWvLNiVP7T3g85e62RTXmuLWImHTUx31nJSbrSckNDyYLxdQaduyrlHfhkP/zDPNmpMuZhTmReUGEgg+41y70x9rc9nNdfHuhooNo/aMdE9qsZ67VV7Cs9yRWwNGhoBDrFhgWGgG7unEoqZtMRUWAH8WIYwPbD8l+SwVAb1HdESL0akK5tBjXiJPOIrVE/3zIJ89YwCiB6rMkgGMta9DmP/Ka9by+i0qK7ZQ==; SRT5=1743171422; BUC=thXGTJBsA6L0f9RlU2nx5bUC5TG8rAGMaSHv6GjL9Bo='
}

payload = {
    "operationName": "getInternationalList",
    "variables": {
        "trip": "OW",
        "itinerary": [{
            "departureAirport": "ICN",
            "arrivalAirport": "OSA",
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
    "query": """
    query getInternationalList($trip: InternationalList_TripType!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: InternationalList_CabinClass!, $where: InternationalList_DeviceType = pc, $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {
      internationalList(
        input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}
      ) {
        galileoKey
        galileoFlag
        travelBizKey
        travelBizFlag
        totalResCnt
        resCnt
        results {
          airlines
          airports
          fareTypes
          schedules
          fares
          errors
        }
      }
    }
    """
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("응답 코드:", response.status_code)
print("응답 내용:", response.text)
