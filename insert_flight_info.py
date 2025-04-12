import cx_Oracle
import pandas as pd


# Oracle DB 연결 설정
def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # 로컬호스트와 SID 사용
    connection = cx_Oracle.connect(user="C##DDD", password="123123", dsn=dsn)
    return connection


# 항공편 데이터를 읽어 DB에 삽입
def insert_flight_data():
    connection = get_db_connection()
    cursor = connection.cursor()

    # flight_info.csv 파일 읽기
    flight_df = pd.read_csv('output/flight_info.csv')

    # 날짜 컬럼을 datetime 형식으로 변환
    flight_df['DEPARTURE_DTM'] = pd.to_datetime(flight_df['DEPARTURE_DTM'], errors='coerce')
    flight_df['ARRIVAL_DTM'] = pd.to_datetime(flight_df['ARRIVAL_DTM'], errors='coerce')
    flight_df['CREATE_AT'] = pd.to_datetime(flight_df['CREATE_AT'], errors='coerce')
    flight_df['UPDATE_AT'] = pd.to_datetime(flight_df['UPDATE_AT'], errors='coerce')

    for index, row in flight_df.iterrows():
        # ID로 이미 존재하는 항공편이 있는지 확인
        cursor.execute("""
            SELECT COUNT(1) FROM C##DDD.FLIGHT_INFO WHERE ID = :ID
        """, {
            "ID": row['ID']
        })

        # 항공편이 존재하지 않으면 삽입
        if cursor.fetchone()[0] == 0:
            # 삽입할 값 출력 (디버깅용)
            print(
                f"Inserting flight data: {row['ID']}, {row['DEPARTURE_DTM']}, {row['ARRIVAL_DTM']}, {row['CODE']}, {row['ROUTE_ID']}, {row['AIRLINE_ID']}, {row['CREATE_AT']}, {row['UPDATE_AT']}, NULL, {row['DELETE_YN']}")

            cursor.execute("""
                INSERT INTO C##DDD.FLIGHT_INFO (ID, DEPARTURE_DTM, ARRIVAL_DTM, CODE, ROUTE_ID, AIRLINE_ID, CREATE_AT, UPDATE_AT, DELETE_AT, DELETE_YN)
                VALUES (:ID, :DEPARTURE_DTM, :ARRIVAL_DTM, :CODE, :ROUTE_ID, :AIRLINE_ID, :CREATE_AT, :UPDATE_AT, NULL, :DELETE_YN)
            """, {
                "ID": row['ID'],
                "DEPARTURE_DTM": row['DEPARTURE_DTM'],
                "ARRIVAL_DTM": row['ARRIVAL_DTM'],
                "CODE": row['CODE'],
                "ROUTE_ID": row['ROUTE_ID'],
                "AIRLINE_ID": row['AIRLINE_ID'],
                "CREATE_AT": row['CREATE_AT'],
                "UPDATE_AT": row['UPDATE_AT'],
                # "DELETE_AT":NULL
                "DELETE_YN": row['DELETE_YN']
            })
        else:
            print(f"항공편 {row['ID']}는 이미 존재합니다. 삽입되지 않았습니다.")

    # 커밋 후 연결 종료
    connection.commit()
    cursor.close()
    connection.close()

    print("✅ 항공편 데이터베이스에 성공적으로 삽입되었습니다!!")


# 실행
if __name__ == "__main__":
    insert_flight_data()
