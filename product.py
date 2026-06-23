from db import connect_db

def view_products():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        p.product_id,
        p.product_name,
        p.price,
        p.quantity,
        c.category_name
    FROM products p
    LEFT JOIN categories c
        ON p.category_id = c.category_id
""")

    rows = cur.fetchall()

    print("\n===== DANH SÁCH SẢN PHẨM =====")
    print(f"{'ID':<5}{'Tên sản phẩm':<25}{'Giá':<15}{'SL':<10}{'Danh mục'}")
    print("-" * 55)

    for row in rows:
        print(f"{row[0]:<5}{row[1]:<25}{float(row[2]):<15.2f}{row[3]:<10}{row[4]}")

    cur.close()
    conn.close()


def add_product():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Tên sản phẩm: ")
    price = float(input("Giá: "))
    quantity = int(input("Số lượng: "))
    category_id = int(input("ID danh mục: "))
    if price <= 0:
        print("Giá phải lớn hơn 0!")
        cur.close()
        conn.close()
        return

    if quantity < 0:
        print("Số lượng không được âm!")
        cur.close()
        conn.close()
        return

    cur.execute(
    """
    INSERT INTO products(product_name, price, quantity, category_id)
    VALUES (%s, %s, %s, %s)
    """,
    (name, price, quantity, category_id)
)

    conn.commit()

    print("Đã thêm sản phẩm!")

    cur.close()
    conn.close()
    
def delete_product():
    conn = connect_db()
    cur = conn.cursor()

    product_id = int(input("Nhập ID sản phẩm cần xóa: "))

    cur.execute(
        """
        DELETE FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    conn.commit()

    print("Đã xóa sản phẩm!")

    cur.close()
    conn.close()

def update_product():
    conn = connect_db()
    cur = conn.cursor()

    product_id = int(input("Nhập ID sản phẩm: "))
    name = input("Tên mới: ")
    price = float(input("Giá mới: "))
    quantity = int(input("Số lượng mới: "))
    category_id = int(input("ID danh mục mới: "))

    if price <= 0:
        print("Giá phải lớn hơn 0!")

        cur.close()
        conn.close()
        return

    if quantity < 0:
        print("Số lượng không được âm!")

        cur.close()
        conn.close()
        return

    cur.execute(
        """
        UPDATE products
        SET product_name = %s,
            price = %s,
            quantity = %s,
            category_id = %s
        WHERE product_id = %s
        """,
        (name, price, quantity, category_id, product_id)
    )

    conn.commit()

    print("Đã cập nhật sản phẩm!")

    cur.close()
    conn.close()

def search_product():
    conn = connect_db()
    cur = conn.cursor()

    keyword = input("Nhập tên sản phẩm cần tìm: ")

    cur.execute(
        """
        SELECT * FROM products
        WHERE product_name ILIKE %s
        """,
        ('%' + keyword + '%',)
    )

    rows = cur.fetchall()

    print("\n===== KẾT QUẢ TÌM KIẾM =====")

    print(f"{'ID':<5}{'Tên sản phẩm':<25}{'Giá':<15}{'SL':<10}")
    print("-" * 55)

    for row in rows:
        print(f"{row[0]:<5}{row[1]:<25}{float(row[2]):<15.2f}{row[3]:<10}")

    cur.close()
    conn.close()

def import_stock():
    conn = connect_db()
    cur = conn.cursor()

    product_id = int(input("Nhập ID sản phẩm: "))
    quantity = int(input("Số lượng nhập thêm: "))
    if quantity <= 0:
        print("Số lượng nhập phải lớn hơn 0!")

        cur.close()
        conn.close()
        return

    cur.execute(
        """
        UPDATE products
        SET quantity = quantity + %s
        WHERE product_id = %s
        """,
        (quantity, product_id)
    )

    cur.execute(
        """
        INSERT INTO imports(product_id, quantity)
        VALUES (%s, %s)
        """,
        (product_id, quantity)
    )

    conn.commit()

    print("Nhập kho thành công!")

    cur.close()
    conn.close()

def export_stock():
    conn = connect_db()
    cur = conn.cursor()

    product_id = int(input("Nhập ID sản phẩm: "))
    quantity = int(input("Số lượng xuất: "))
    if quantity <= 0:
        print("Số lượng xuất phải lớn hơn 0!")

        cur.close()
        conn.close()
        return

    # Kiểm tra sản phẩm có tồn tại không
    cur.execute(
        """
        SELECT quantity
        FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    result = cur.fetchone()

    if result is None:
        print("Không tìm thấy sản phẩm!")

        cur.close()
        conn.close()
        return

    current_quantity = result[0]

    # Kiểm tra tồn kho
    if quantity > current_quantity:
        print("Không đủ hàng trong kho!")

        cur.close()
        conn.close()
        return

    # Xuất kho
    cur.execute(
        """
        UPDATE products
        SET quantity = quantity - %s
        WHERE product_id = %s
        """,
        (quantity, product_id)
    )

    # Lưu lịch sử xuất kho
    cur.execute(
        """
        INSERT INTO exports(product_id, quantity)
        VALUES (%s, %s)
        """,
        (product_id, quantity)
    )

    conn.commit()

    print("Xuất kho thành công!")

    cur.close()
    conn.close()

def inventory_report():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*),
            SUM(quantity),
            SUM(price * quantity)
        FROM products
    """)

    result = cur.fetchone()

    print("\n===== THỐNG KÊ KHO =====")
    print("Tổng số sản phẩm:", result[0])
    print("Tổng số lượng hàng:", result[1])
    print("Tổng giá trị kho:", result[2])

    cur.close()
    conn.close()

def view_categories():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM categories")

    rows = cur.fetchall()

    print("\n===== DANH SÁCH DANH MỤC =====")

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def add_category():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Tên danh mục: ")

    cur.execute(
        """
        INSERT INTO categories(category_name)
        VALUES (%s)
        """,
        (name,)
    )

    conn.commit()

    print("Đã thêm danh mục!")

    cur.close()
    conn.close()

def delete_category():
    conn = connect_db()
    cur = conn.cursor()

    category_id = int(input("ID danh mục cần xóa: "))

    cur.execute(
        """
        DELETE FROM categories
        WHERE category_id = %s
        """,
        (category_id,)
    )

    conn.commit()

    print("Đã xóa danh mục!")

    cur.close()
    conn.close()

