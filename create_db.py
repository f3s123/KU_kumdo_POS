# 데이터 초기화 희망 시 실행

import sqlite3
import json
from datetime import datetime

# 데이터베이스 파일 생성
db_path = "kendo_bar.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_tables():
    # SQLite connection with Korean support
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA encoding = 'UTF-8'")
    
    # Enable Korean text output
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    conn.row_factory = dict_factory
    conn.text_factory = str
    cur = conn.cursor()

    # Pragma 설정으로 한글 인코딩 지원
    cur.execute("PRAGMA encoding = 'UTF-8'")

    # orders 테이블 생성 (실시간 주문 관리)
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_num INTEGER NOT NULL,
        menu_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        time TEXT NOT NULL,
        etc TEXT
    )
    """)

    # table_orders 테이블 생성 (테이블별 현재 상태)
    cur.execute("DROP TABLE IF EXISTS table_orders")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS table_orders (
        table_num INTEGER PRIMARY KEY,
        tbl_orders TEXT NOT NULL,
        people INTEGER DEFAULT 0,
        total_price INTEGER DEFAULT 0,
        memo TEXT,
        entrance_time TEXT,
        end_time TEXT
    )
    """)

    # menu 테이블 생성
    cur.execute("DROP TABLE IF EXISTS menu")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        menu_json TEXT NOT NULL
    )
    """)

    # menu_to 테이블 생성
    cur.execute("DROP TABLE IF EXISTS menu_to")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS menu_to (
        menu_json TEXT
    )
    ''')

    # done_orders 테이블 생성 (완료된 주문)
    cur.execute("DROP TABLE IF EXISTS done_orders")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS done_orders (
        done_id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_num INTEGER NOT NULL,
        menu TEXT NOT NULL,
        order_time TEXT NOT NULL,
        done_time TEXT NOT NULL
    )
    """)

    # deleted_orders 테이블 생성 (취소된 주문)
    cur.execute("DROP TABLE IF EXISTS deleted_orders")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deleted_orders (
        delete_id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_num INTEGER NOT NULL,
        menu TEXT NOT NULL,
        order_time TEXT NOT NULL,
        delete_time TEXT NOT NULL
    )
    """)

    # payments 테이블 생성 (결제 내역)
    cur.execute("DROP TABLE IF EXISTS payments")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_num INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        payment_time TEXT NOT NULL,
        memo TEXT,
        detail TEXT,
        entrance_time TEXT,
        end_time TEXT,
        used_time TEXT,           /* 실제 사용 시간 (00시 00분 00초 형식) */
        used_seconds INTEGER      /* 실제 사용 시간 (초 단위) */
    )
    """)

    conn.commit()
    conn.close()

def insert_initial_data():
    # SQLite connection with Korean support
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA encoding = 'UTF-8'")
    conn.text_factory = str
    cur = conn.cursor()

    # 메뉴 데이터 삽입
    menu_data = {
        "menus": [
            {"name": "타코야끼 (데리야끼)", "price": 8500},
            {"name": "타코야끼 (불닭)", "price": 8500},
            {"name": "야끼소바 (간장)", "price": 12000},
            {"name": "야끼소바 (불닭)", "price": 12000},
            {"name": "우삼겹숙주볶음", "price": 16000},
            {"name": "나가사키해물우동", "price": 10000},
            {"name": "흑당인절미 당고", "price": 6500},
            {"name": "황도", "price": 10000},
            {"name": "교자", "price": 8000},
            {"name": "메론소다", "price": 4000},
            {"name": "청포도 에이드", "price": 4000},
            {"name": "망고 에이드", "price": 4000},
            {"name": "아망추", "price": 5500},
            {"name": "선라이즈", "price": 6000},
            {"name": "로이 로저스", "price": 6000},
            {"name": "신데렐라", "price": 6000},
            {"name": "하이볼 키트", "price": 4000},
            {"name": "입장료 + 자릿세", "price": 5000},
            {"name": "콜키지 1L 미만", "price": 3000},
            {"name": "콜키지 1L 이상", "price": 6000}
        ]
    }

    # Insert menu data with UTF-8 encoding
    menu_json = json.dumps(menu_data, ensure_ascii=False).encode('utf-8').decode('utf-8')
    cur.execute("INSERT INTO menu (menu_json) VALUES (?)", (menu_json,))

    menu_to_data = {
        "menus": [
            { "name": "타코야끼 (데리야끼)", "price": 6500 },
            { "name": "타코야끼 (불닭)", "price": 6500 },
            { "name": "야끼소바 (간장)", "price": 10000 },
            { "name": "야끼소바 (불닭)", "price": 10000 },
            { "name": "우삼겹숙주볶음", "price": 14000 },
            { "name": "흑당인절미 당고", "price": 5500 },
            { "name": "메론소다", "price": 3000 },
            { "name": "청포도 에이드", "price": 3000 },
            { "name": "망고 에이드", "price": 3000 },
            { "name": "아망추", "price": 4500 },
            { "name": "선라이즈", "price": 5000 },
            { "name": "로이 로저스", "price": 5000 },
            { "name": "신데렐라", "price": 5000 }
        ]
    }

    # Insert menu data with UTF-8 encoding
    menu_to_json = json.dumps(menu_to_data, ensure_ascii=False).encode('utf-8').decode('utf-8')
    cur.execute("INSERT INTO menu_to (menu_json) VALUES (?)", (menu_to_json,))

    # Initial orders data
    initial_orders = {
        "타코야끼 (데리야끼)": 0,
        "타코야끼 (불닭)": 0,
        "야끼소바 (간장)": 0,
        "야끼소바 (불닭)": 0,
        "우삼겹숙주볶음": 0,
        "나가사키해물우동": 0,
        "흑당인절미 당고": 0,
        "황도": 0,
        "교자": 0,
        "메론소다": 0,
        "청포도 에이드": 0,
        "망고 에이드": 0,
        "아망추": 0,
        "선라이즈": 0,
        "로이 로저스": 0,
        "신데렐라": 0,
        "하이볼 키트": 0,
        "입장료 + 자릿세": 0,
        "콜키지 1L 미만": 0,
        "콜키지 1L 이상": 0
    }

    # Insert table orders with UTF-8 encoding
    orders_json = json.dumps(initial_orders, ensure_ascii=False).encode('utf-8').decode('utf-8')
    
    for table_num in range(1, 19):  # 1번부터 18번 테이블
        cur.execute("""
        INSERT INTO table_orders (table_num, tbl_orders, people, total_price, memo, entrance_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (table_num, orders_json, 0, 0, "", "", ""))

    conn.commit()
    conn.close()

def initialize_database():
    print(f"Creating database: {db_path}")
    create_tables()
    print("Tables created successfully")
    insert_initial_data()
    print("Initial data inserted successfully")
    print(f"Database '{db_path}' has been initialized successfully!")

if __name__ == "__main__":
    initialize_database()