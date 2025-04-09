import cx_Oracle
import pandas as pd


# Oracle DB 연결 설정
def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # 로컬호스트와 SID 사용
    connection = cx_Oracle.connect(user="C##DDD", password="123123", dsn=dsn)
    return connection


# CSV 데이터를 읽어 DB에 삽입
def insert_data_to_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    # flight_info.csv 파일 읽기
    flight_df = pd.read_csv('flight_info.csv')

    # flight_info 테이블에 데이터 삽입
    for index, row in flight_df.iterrows():
        cursor.execute("""
            INSERT INTO C##DDD.FLIGHT_INFO (DEPARTURE_DTM, ARRIVAL_DTM, CODE, ROUTE_ID, AIRLINE_ID, CREATE_AT, UPDATE_AT, DELETE_AT, DELETE_YN)
            VALUES (:DEPARTURE_DTM, :ARRIVAL_DTM, :CODE, :ROUTE_ID, :AIRLINE_ID, :CREATE_AT, :UPDATE_AT, :DELETE_AT, :DELETE_YN)
        """, {
            "DEPARTURE_DTM": row['DEPARTURE_DTM'],
            "ARRIVAL_DTM": row['ARRIVAL_DTM'],
            "CODE": row['CODE'],
            "ROUTE_ID": row['ROUTE_ID'],
            "AIRLINE_ID": row['AIRLINE_ID'],
            "CREATE_AT": row['CREATE_AT'],
            "UPDATE_AT": row['UPDATE_AT'],
            "DELETE_AT": row['DELETE_AT'],
            "DELETE_YN": row['DELETE_YN']
        })

    # # price_info.csv 파일 읽기
    # price_df = pd.read_csv('price_info.csv')
    # 
    # # price_info 테이블에 데이터 삽입
    # for index, row in price_df.iterrows():
    #     cursor.execute("""
    #         INSERT INTO C##DDD.PRICE_INFO (SEARCH_DATE, PRICE, FLIGHT_INFO_ID, CREATE_AT, UPDATE_AT, DELETE_AT, DELETE_YN)
    #         VALUES (:SEARCH_DATE, :PRICE, :FLIGHT_INFO_ID, :CREATE_AT, :UPDATE_AT, :DELETE_AT, :DELETE_YN)
    #     """, {
    #         "SEARCH_DATE": row['SEARCH_DATE'],
    #         "PRICE": row['PRICE'],
    #         "FLIGHT_INFO_ID": row['FLIGHT_INFO_ID'],
    #         "CREATE_AT": row['CREATE_AT'],
    #         "UPDATE_AT": row['UPDATE_AT'],
    #         "DELETE_AT": row['DELETE_AT'],
    #         "DELETE_YN": row['DELETE_YN']
    #     })

    # 커밋 후 연결 종료
    connection.commit()
    cursor.close()
    connection.close()

    print("✅ 데이터베이스에 성공적으로 삽입되었습니다!")


# 실행
if __name__ == "__main__":
    insert_data_to_db()
