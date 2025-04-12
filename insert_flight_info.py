import cx_Oracle
import pandas as pd


# Oracle DB 연결 설정
def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # 로컬호스트와 SID 사용
    connection = cx_Oracle.connect(user="C##DDD", password="123123", dsn=dsn)
    return connection


# 가격 데이터를 읽어 DB에 삽입
def insert_price_data():
    connection = get_db_connection()
    cursor = connection.cursor()

    # price_info.csv 파일 읽기
    price_df = pd.read_csv('output/price_info.csv')

    # 날짜 컬럼을 datetime 형식으로 변환
    price_df['SEARCH_DATE'] = pd.to_datetime(price_df['SEARCH_DATE'], errors='coerce')
    price_df['CREATE_AT'] = pd.to_datetime(price_df['CREATE_AT'], errors='coerce')
    price_df['UPDATE_AT'] = pd.to_datetime(price_df['UPDATE_AT'], errors='coerce')

    for index, row in price_df.iterrows():
        # 가격 데이터를 PRICE_INFO 테이블에 삽입
        cursor.execute("""
            INSERT INTO C##DDD.PRICE_INFO (SEARCH_DATE, PRICE, FLIGHT_INFO_ID, CREATE_AT, UPDATE_AT, DELETE_AT, DELETE_YN)
            VALUES (:SEARCH_DATE, :PRICE, :FLIGHT_INFO_ID, :CREATE_AT, :UPDATE_AT, :DELETE_AT, :DELETE_YN)
        """, {
            "SEARCH_DATE": row['SEARCH_DATE'],
            "PRICE": row['PRICE'],
            "FLIGHT_INFO_ID": row['FLIGHT_INFO_ID'],
            "CREATE_AT": row['CREATE_AT'],
            "UPDATE_AT": row['UPDATE_AT'],
            "DELETE_AT": None,  # DELETE_AT을 NULL로 설정
            "DELETE_YN": row['DELETE_YN']
        })

    # 커밋 후 연결 종료
    connection.commit()
    cursor.close()
    connection.close()

    print("✅ 가격 데이터베이스에 성공적으로 삽입되었습니다!!")


# 실행
if __name__ == "__main__":
    insert_price_data()