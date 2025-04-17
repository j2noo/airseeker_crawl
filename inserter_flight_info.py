import cx_Oracle
import pandas as pd
import sys

def insert_flight_data(file_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    # flight_info.csv 파일 읽기
    flight_df = pd.read_csv(file_name)

    # 날짜 컬럼을 datetime 형식으로 변환
    flight_df['DEPARTURE_DTM'] = pd.to_datetime(flight_df['DEPARTURE_DTM'], errors='coerce')
    flight_df['ARRIVAL_DTM'] = pd.to_datetime(flight_df['ARRIVAL_DTM'], errors='coerce')
    flight_df['CREATE_AT'] = pd.to_datetime(flight_df['CREATE_AT'], errors='coerce')
    flight_df['UPDATE_AT'] = pd.to_datetime(flight_df['UPDATE_AT'], errors='coerce')

    # ✅ AIRLINE 테이블에서 CODE → ID 매핑 딕셔너리 만들기
    cursor.execute("SELECT ID, CODE FROM C##DDD.AIRLINE")
    airline_rows = cursor.fetchall()
    airline_map = {code: id for id, code in airline_rows}

    # ✅ flight_df['AIRLINE_ID']는 코드임 → 숫자 ID로 매핑
    flight_df['AIRLINE_ID'] = flight_df['AIRLINE_ID'].map(airline_map)

    # ✅ 매핑되지 않은 코드가 있으면 경고 출력 후 종료
    if flight_df['AIRLINE_ID'].isnull().any():
        missing = flight_df[flight_df['AIRLINE_ID'].isnull()]
        print("❌ 매핑되지 않은 항공사 코드가 있습니다:")
        print(missing[['CODE']].drop_duplicates())
        sys.exit(1)

    for _, row in flight_df.iterrows():
        # 중복 체크
        cursor.execute("""
            SELECT COUNT(1) FROM C##DDD.FLIGHT_INFO WHERE ID = :ID
        """, {"ID": row['ID']})

        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO C##DDD.FLIGHT_INFO (
                    ID, DEPARTURE_DTM, ARRIVAL_DTM, CODE,
                    ROUTE_ID, AIRLINE_ID, CREATE_AT, UPDATE_AT,
                    DELETE_AT, DELETE_YN
                )
                VALUES (
                    :ID, :DEPARTURE_DTM, :ARRIVAL_DTM, :CODE,
                    :ROUTE_ID, :AIRLINE_ID, :CREATE_AT, :UPDATE_AT,
                    NULL, :DELETE_YN
                )
            """, {
                "ID": row['ID'],
                "DEPARTURE_DTM": row['DEPARTURE_DTM'],
                "ARRIVAL_DTM": row['ARRIVAL_DTM'],
                "CODE": row['CODE'],
                "ROUTE_ID": row['ROUTE_ID'],
                "AIRLINE_ID": row['AIRLINE_ID'],
                "CREATE_AT": row['CREATE_AT'],
                "UPDATE_AT": row['UPDATE_AT'],
                "DELETE_YN": row['DELETE_YN']
            })

    connection.commit()
    cursor.close()
    connection.close()

    print("✅ 항공편 데이터베이스에 성공적으로 삽입되었습니다!!\n")


def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
    return cx_Oracle.connect(user="C##DDD", password="123123", dsn=dsn)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("$python starter.py 를 통해 실행하세요")
        sys.exit(1)

    file_name = sys.argv[1]
    insert_flight_data(file_name)
