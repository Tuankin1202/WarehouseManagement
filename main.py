from product import (
    view_products,
    add_product,
    delete_product,
    update_product,
    search_product,
    import_stock,
    export_stock,
    inventory_report,
    view_categories,
    add_category,
    delete_category
)
from auth import login
if not login():
    exit()
    
while True:

    print("\n===== QUẢN LÝ KHO =====")
    print("1. Xem sản phẩm")
    print("2. Thêm sản phẩm")
    print("3. Xóa sản phẩm")
    print("4. Cập nhật sản phẩm")
    print("5. Tìm kiếm sản phẩm")
    print("6. Nhập kho")
    print("7. Xuất kho")
    print("8. Thống kê kho")
    print("9. Xem danh mục")
    print("10. Thêm danh mục")
    print("11. Xóa danh mục")
    print("0. Thoát")

    choice = input("Chọn: ")

    if choice == "1":
        view_products()

    elif choice == "2":
        add_product()

    elif choice == "3":
        delete_product()

    elif choice == "4":
        update_product()

    elif choice == "5":
        search_product()

    elif choice == "6":
        import_stock()

    elif choice == "7":
        export_stock()

    elif choice == "8":
        inventory_report()

    elif choice == "9":
        view_categories()

    elif choice == "10":
        add_category()

    elif choice == "11":
        delete_category()       

    elif choice == "0":
        print("Tạm biệt!")
        break

    else:
        print("Lựa chọn không hợp lệ!")