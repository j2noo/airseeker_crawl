import cx_Oracle
import pandas as pd
import sys

def insert_airline_data(file_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    # airline.csv 읽기
    airline_df = pd.read_csv(file_name)

    # 날짜 컬럼을 datetime 형식으로 변환
    airline_df['CREATE_AT'] = pd.to_datetime(airline_df['CREATE_AT'], errors='coerce')
    airline_df['UPDATE_AT'] = pd.to_datetime(airline_df['UPDATE_AT'], errors='coerce')

    for _, row in airline_df.iterrows():
        # 이미 존재하는 CODE인지 확인
        cursor.execute("""
            SELECT COUNT(1) FROM C##DDD.AIRLINE WHERE CODE = :CODE
        """, {"CODE": row['CODE']})

        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO C##DDD.AIRLINE (CODE, NAME, KOREAN_YN, CREATE_AT, UPDATE_AT, DELETE_AT, DELETE_YN)
                VALUES (:CODE, :NAME, :KOREAN_YN, :CREATE_AT, :UPDATE_AT, NULL, :DELETE_YN)
            """, {
                "CODE": row['CODE'],
                "NAME": row['NAME'],
                "KOREAN_YN": row['KOREAN_YN'],
                "CREATE_AT": row['CREATE_AT'],
                "UPDATE_AT": row['UPDATE_AT'],
                "DELETE_YN": row['DELETE_YN']
            })

    connection.commit()
    cursor.close()
    connection.close()

    print("✅ 항공사 데이터베이스에 성공적으로 삽입되었습니다!!\n")

def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
    return cx_Oracle.connect(user="C##DDD", password="123123", dsn=dsn)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("$python starter.py 를 통해 실행하세요")
        sys.exit(1)

    file_name = sys.argv[1]
    insert_airline_data(file_name)
