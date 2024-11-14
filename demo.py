from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Cập nhật Service cho ChromeDriver
service = Service(ChromeDriverManager().install())

# Khởi tạo ChromeDriver với Service
driver = webdriver.Chrome(service=service)

try:
    # Mở trang Google
    driver.get("https://www.google.com")

    # Chờ trang tải xong
    time.sleep(2)

    # Tìm ô tìm kiếm trên Google và nhập từ khóa "du học Mỹ"
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("du học Mỹ")
    search_box.send_keys(Keys.RETURN)  # Thay cho submit() bằng RETURN (enter)

    # Đợi kết quả tìm kiếm hiển thị
    time.sleep(3)

    # Số trang tìm kiếm tối đa
    max_pages = 5
    current_page = 1

    # Duyệt qua tối đa 5 trang tìm kiếm
    while current_page <= max_pages:
        print(f"Đang kiểm tra trang {current_page}...")

        # Lấy tất cả các liên kết trong kết quả tìm kiếm trên trang hiện tại
        links = driver.find_elements(By.XPATH, "//h3/../a")

        # Kiểm tra từng liên kết
        for link in links:
            url = link.get_attribute("href")  # Lấy URL của từng liên kết
            if url == "https://duhocvietphuong.edu.vn/":
                print("Đã tìm thấy URL: https://duhocvietphuong.edu.vn/")
                link.click()  # Nhấp vào liên kết
                time.sleep(5)  # Chờ để đảm bảo trang tải đầy đủ
                break

        # Nếu không tìm thấy URL trong trang hiện tại, chuyển sang trang tiếp theo
        if driver.current_url != "https://duhocvietphuong.edu.vn/":
            try:
                # Tìm nút chuyển trang tiếp theo bằng XPath
                next_page_button = driver.find_element(By.XPATH, "//a[@aria-label='Page 2']")
                next_page_button.click()  # Nhấp vào liên kết chuyển sang trang 2
                current_page += 1
                time.sleep(3)  # Đợi trang tiếp theo tải

                # Kiểm tra các kết quả tìm kiếm trên trang mới
                cites = driver.find_elements(By.XPATH, "//cite[contains(text(),'duhocvietphuong.edu.vn')]")
                for cite in cites:
                    url = cite.text
                    if "https://duhocvietphuong.edu.vn" in url:
                        print(f"Đã tìm thấy URL trong cite: {url}")
                        # Nhấp vào liên kết chứa URL
                        parent_link = cite.find_element(By.XPATH, "..")  # Tìm phần tử cha của cite (liên kết)
                        parent_link.click()
                        time.sleep(5)  # Chờ để đảm bảo trang tải đầy đủ
                        break

            except Exception as e:
                print("Không thể tìm thấy nút 'Tiếp', kết thúc tìm kiếm.")
                break
        else:
            # Kiểm tra trang đã tải đầy đủ chưa
            print("Trang đã tải xong. Bắt đầu cuộn trang...")
            time.sleep(3)

            # Cuộn xuống dưới cùng
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Cuộn lên trên cùng
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)

            # Cuộn một đoạn nhỏ (ví dụ, cuộn xuống một nửa trang)
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(3)

            # Cuộn lại lên trên
            driver.execute_script("window.scrollBy(0, -500);")
            time.sleep(3)

            # Thực hiện thêm cuộn nếu cần thiết
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 1000);")  # Cuộn xuống 1000px
                time.sleep(2)  # Chờ thời gian sau mỗi cuộn

            break

    # Đợi trang duhocvietphuong.edu.vn tải xong và giữ lại trong 120 giây (2 phút)
    time.sleep(120)

finally:
    # Đảm bảo rằng trình duyệt sẽ đóng lại khi kết thúc
    driver.quit()
