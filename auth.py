from db import connect_db

def login():

    conn = connect_db()
    cur = conn.cursor()

    username = input("Tên đăng nhập: ")
    password = input("Mật khẩu: ")

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username = %s
        AND password = %s
        """,
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        print("Đăng nhập thành công!")
        return True

    print("Sai tài khoản hoặc mật khẩu!")
    return False