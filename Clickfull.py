# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# # Cài đặt Service cho ChromeDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

# # Mở trình duyệt ở chế độ toàn màn hình
# driver.maximize_window()

# # Hàm tìm kiếm và cuộn trang nếu tìm thấy URL yêu cầu
# def tim_kiem_va_cuon_trang(tu_khoa):
#     try:
#         # Mở Google và nhập từ khóa tìm kiếm
#         driver.get("https://www.google.com")
#         time.sleep(2)  # Chờ trang tải
#         search_box = driver.find_element(By.NAME, "q")
#         search_box.send_keys(tu_khoa)
#         search_box.send_keys(Keys.RETURN)
#         time.sleep(3)  # Chờ kết quả hiển thị

#         max_pages = 5
#         current_page = 1
#         found = False

#         while current_page <= max_pages:
#             print(f"Đang kiểm tra trang {current_page}...")

#             # Kiểm tra các phần tử <cite> để tìm URL chứa "duhocvietphuong.edu.vn"
#             cites = driver.find_elements(By.XPATH, "//cite")
#             for cite in cites:
#                 url = cite.text
#                 if "duhocvietphuong.edu.vn" in url:
#                     print(f"Đã tìm thấy URL trong cite: {url}")
#                     # Tìm phần tử cha của <cite> để click vào liên kết
#                     parent_link = cite.find_element(By.XPATH, "..")
#                     parent_link.click()
#                     time.sleep(5)  # Đợi trang tải đầy đủ
#                     found = True
#                     break

#             if found:
#                 break

#             # Nếu không tìm thấy, chuyển sang trang tiếp theo
#             try:
#                 next_page_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
#                 next_page_button.click()
#                 current_page += 1
#                 time.sleep(3)
#             except Exception:
#                 print("Không tìm thấy nút 'Tiếp', kết thúc tìm kiếm.")
#                 break

#         if found:
#             # Cuộn lên và xuống liên tục trong 120 giây
#             print("Trang đã tải xong. Bắt đầu cuộn lên và xuống trong 120 giây...")
#             start_time = time.time()
#             scroll_direction = "down"  # Ban đầu cuộn xuống
#             while time.time() - start_time < 120:
#                 if scroll_direction == "down":
#                     driver.execute_script("window.scrollBy(0, 200);")  # Cuộn xuống 200px
#                     if driver.execute_script("return window.innerHeight + window.scrollY") >= driver.execute_script("return document.body.scrollHeight"):
#                         scroll_direction = "up"  # Đổi chiều nếu đạt cuối trang
#                 else:
#                     driver.execute_script("window.scrollBy(0, -200);")  # Cuộn lên 200px
#                     if driver.execute_script("return window.scrollY") == 0:
#                         scroll_direction = "down"  # Đổi chiều nếu đạt đầu trang
#                 time.sleep(0.5)  # Chờ 0.5 giây rồi tiếp tục cuộn

#         else:
#             print(f"Không tìm thấy URL 'duhocvietphuong.edu.vn' cho từ khóa '{tu_khoa}'.")

#     except Exception as e:
#         print(f"Lỗi xảy ra khi tìm kiếm từ khóa '{tu_khoa}': {e}")

# # Thực hiện tìm kiếm cho các từ khóa lần lượt
# try:
#     tim_kiem_va_cuon_trang("du học Mỹ")
#     tim_kiem_va_cuon_trang("du học Canada")

# finally:
#     driver.quit()


