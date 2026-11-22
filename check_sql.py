"""Manual SQLite inspection utility."""

import sqlite3
from pathlib import Path

from database.db_setup import DEFAULT_DB_PATH, initialize_database


def get_tables(connection: sqlite3.Connection) -> list[str]:
    """Return all application and SQLite metadata table names."""
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    return [str(row["name"]) for row in rows]


def print_table_info(connection: sqlite3.Connection, table_name: str) -> None:
    """Print a table's columns and up to 100 rows."""
    if not table_name.replace("_", "").isalnum():
        print("資料表名稱只能包含英文字母、數字與底線。")
        return

    exists = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    if not exists:
        print(f"找不到資料表：{table_name}")
        return

    columns = connection.execute(f"PRAGMA table_info('{table_name}')").fetchall()
    print(f"\n資料表：{table_name}")
    print("欄位：")
    for column in columns:
        print(
            f"  - {column['name']} "
            f"({column['type'] or '未指定'}"
            f"{', PRIMARY KEY' if column['pk'] else ''}"
            f"{', NOT NULL' if column['notnull'] else ''})"
        )

    rows = connection.execute(f'SELECT * FROM "{table_name}" LIMIT 100').fetchall()
    print(f"資料筆數（最多顯示 100 筆）：{len(rows)}")
    for row in rows:
        print(dict(row))


def execute_read_only(connection: sqlite3.Connection, sql: str) -> None:
    """Execute a read-only SQL statement and print the result."""
    normalized = sql.lstrip().upper()
    if not normalized.startswith(("SELECT", "WITH", "PRAGMA")):
        print("只允許執行 SELECT、WITH 或 PRAGMA 查詢。")
        return

    try:
        rows = connection.execute(sql).fetchall()
    except sqlite3.Error as exc:
        print(f"SQL 錯誤：{exc}")
        return

    if not rows:
        print("查詢成功，沒有資料。")
        return

    for row in rows:
        print(dict(row))


def main() -> None:
    """Start the interactive SQLite inspection menu."""
    database_path = DEFAULT_DB_PATH
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    print("SQLite 檢查工具")
    print(f"資料庫：{database_path}")

    try:
        while True:
            print("\n請選擇操作：")
            print("1. 列出資料表")
            print("2. 查看資料表內容")
            print("3. 執行 SQL 查詢")
            print("4. 離開")
            choice = input("選項：").strip()

            if choice == "1":
                tables = get_tables(connection)
                if tables:
                    for table in tables:
                        print(f"- {table}")
                else:
                    print("目前沒有資料表。")
            elif choice == "2":
                print("可用資料表：" + ", ".join(get_tables(connection)))
                table_name = input("輸入資料表名稱：").strip()
                print_table_info(connection, table_name)
            elif choice == "3":
                sql = input("輸入 SELECT SQL：").strip()
                if sql:
                    execute_read_only(connection, sql)
            elif choice == "4":
                break
            else:
                print("請輸入 1 到 4。")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
