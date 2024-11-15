from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Cài đặt Service cho ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Mở Google
    driver.get("https://www.google.com")
    time.sleep(2)  # Chờ trang tải

    # Tìm ô tìm kiếm và nhập từ khóa
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("du học Mỹ")
    search_box.send_keys(Keys.RETURN)  # Nhấn Enter để tìm kiếm
    time.sleep(3)  # Chờ kết quả hiển thị

    # Số trang tối đa cần tìm kiếm
    max_pages = 5
    current_page = 1
    found = False

    while current_page <= max_pages:
        print(f"Đang kiểm tra trang {current_page}...")

        # Kiểm tra tất cả các phần tử <cite> để tìm URL chứa "duhocvietphuong.edu.vn"
        cites = driver.find_elements(By.XPATH, "//cite")
        for cite in cites:
            url = cite.text
            if "duhocvietphuong.edu.vn" in url:
                print(f"Đã tìm thấy URL trong cite: {url}")
                # Tìm phần tử cha của <cite> để click vào liên kết
                parent_link = cite.find_element(By.XPATH, "..")
                parent_link.click()
                time.sleep(5)  # Đợi trang tải đầy đủ
                found = True
                break

        if found:
            break
        
        # Nếu không tìm thấy, chuyển sang trang tiếp theo
        try:
            next_page_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
            next_page_button.click()
            current_page += 1
            time.sleep(3)  # Đợi trang mới tải
        except Exception:
            print("Không tìm thấy nút 'Tiếp', kết thúc tìm kiếm.")
            break

    if not found:
        print("Không tìm thấy URL 'duhocvietphuong.edu.vn' trong kết quả tìm kiếm.")
    else:
        # Cuộn trang mượt khi đã tìm thấy trang đích
        print("Trang đã tải xong. Bắt đầu cuộn trang mượt...")

        # Cuộn xuống từ từ
        for i in range(10):
            driver.execute_script("window.scrollBy(0, 1000);")  # Cuộn xuống 200px
            time.sleep(0.5)  # Thời gian chờ để cuộn mượt

        # Cuộn lên từ từ
        for i in range(10):
            driver.execute_script("window.scrollBy(0, -1000);")  # Cuộn lên 200px
            time.sleep(0.5)  # Thời gian chờ để cuộn mượt

        # Giữ trang trong 500 giây
        time.sleep(120)

finally:
    # Đảm bảo trình duyệt đóng lại khi kết thúc
    driver.quit()
