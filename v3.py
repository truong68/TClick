from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Cập nhật Service cho ChromeDriver
service = Service(ChromeDriverManager().install())

# Cấu hình ChromeOptions để tắt log không cần thiết
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Chỉ hiển thị lỗi, không có thông báo thông thường hoặc cảnh báo

# Khởi tạo ChromeDriver với Service và các tùy chọn
driver = webdriver.Chrome(service=service, options=chrome_options)

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
            if url == "https://think.edu.vn":
                print("Đã tìm thấy URL: https://think.edu.vn")
                link.click()  # Nhấp vào liên kết
                time.sleep(5)  # Chờ để đảm bảo trang tải đầy đủ
                break  # Thoát khỏi vòng lặp tìm kiếm ngay khi đã tìm thấy URL

        # Nếu đã tìm thấy URL, dừng việc tìm kiếm các trang khác và cuộn trang
        if driver.current_url == "https://think.edu.vn":
            print("Trang đã mở: https://think.edu.vn")
            start_time = time.time()

            # Kiểm tra trạng thái trang đã tải hoàn toàn chưa
            while time.time() - start_time < 300:
                # Kiểm tra trang đã tải hoàn toàn
                is_ready = driver.execute_script('return document.readyState') == 'complete'
                if is_ready:
                    # Cuộn trang liên tục trong 300 giây (5 phút)
                    driver.execute_script("window.scrollBy(0, 1000);")  # Cuộn xuống 1000px
                    time.sleep(2)  # Chờ một chút trước khi cuộn tiếp
                else:
                    print("Trang chưa tải hoàn tất, đợi...")
                    time.sleep(2)  # Chờ trước khi kiểm tra lại

            break  # Dừng vòng lặp khi đã hoàn thành việc cuộn trang

        # Nếu không tìm thấy URL trong trang hiện tại, chuyển sang trang tiếp theo
        if driver.current_url != "https://think.edu.vn":
            try:
                # Tìm nút chuyển trang tiếp theo bằng XPath
                next_page_button = driver.find_element(By.XPATH, "//a[@aria-label='Page 2']")
                next_page_button.click()  # Nhấp vào liên kết chuyển sang trang 2
                current_page += 1
                time.sleep(3)  # Đợi trang tiếp theo tải

                # Kiểm tra các kết quả tìm kiếm trên trang mới
                cites = driver.find_elements(By.XPATH, "//cite[contains(text(),'https://think.edu.vn')]")
                for cite in cites:
                    url = cite.text
                    if "https://think.edu.vn" in url:
                        print(f"Đã tìm thấy URL trong cite: {url}")
                        # Nhấp vào liên kết chứa URL
                        parent_link = cite.find_element(By.XPATH, "..")  # Tìm phần tử cha của cite (liên kết)
                        parent_link.click()
                        time.sleep(5)  # Chờ để đảm bảo trang tải đầy đủ
                        break

                # Nếu tìm thấy URL, dừng lại và thực hiện cuộn trang
                if driver.current_url == "https://think.edu.vn":
                    print("Trang đã mở: https://think.edu.vn")
                    start_time = time.time()

                    # Kiểm tra trạng thái trang đã tải hoàn toàn chưa
                    while time.time() - start_time < 300:
                        # Kiểm tra trang đã tải hoàn tất
                        is_ready = driver.execute_script('return document.readyState') == 'complete'
                        if is_ready:
                            # Cuộn trang liên tục trong 300 giây (5 phút)
                            driver.execute_script("window.scrollBy(0, 1000);")  # Cuộn xuống 1000px
                            time.sleep(2)  # Chờ một chút trước khi cuộn tiếp
                        else:
                            print("Trang chưa tải hoàn tất, đợi...")
                            time.sleep(2)  # Chờ trước khi kiểm tra lại

                    break  # Dừng vòng lặp khi đã hoàn thành việc cuộn trang

            except Exception as e:
                print("Không thể tìm thấy nút 'Tiếp', kết thúc tìm kiếm.")
                break

    # Trình duyệt sẽ không tự động đóng, chỉ dừng lại khi cuộn xong
    print("Trình duyệt vẫn đang mở...")
    # Bạn có thể làm gì đó thêm ở đây nếu cần, như kiểm tra giao diện hoặc tiếp tục thao tác.

finally:
    # Không đóng trình duyệt tại đây, chỉ giữ trình duyệt mở.
    pass
