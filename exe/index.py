import re
import time
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Hàm kiểm tra URL hợp lệ
def is_valid_url(url):
    url_pattern = re.compile(r"^(https?://)")
    return url_pattern.match(url)

# Hàm để tìm kiếm từ khóa và cuộn trang
def tim_kiem_va_cuon_trang(driver, tu_khoa):
    # Mở Google và tìm kiếm từ khóa
    driver.get("https://www.google.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(tu_khoa)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    max_pages = 5
    current_page = 1
    found = False

    # Tìm kiếm URL "duhocvietphuong.edu.vn"
    while current_page <= max_pages:
        print(f"Đang kiểm tra trang {current_page}...")

        cites = driver.find_elements(By.XPATH, "//cite")
        for cite in cites:
            url = cite.text
            if "duhocvietphuong.edu.vn" in url:
                print(f"Đã tìm thấy URL trong cite: {url}")
                parent_link = cite.find_element(By.XPATH, "..")
                parent_link.click()
                time.sleep(5)
                found = True
                break

        if found:
            break

        try:
            next_page_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
            next_page_button.click()
            current_page += 1
            time.sleep(3)
        except:
            print("Không tìm thấy nút 'Tiếp', kết thúc tìm kiếm.")
            break

    if not found:
        print("Không tìm thấy URL 'duhocvietphuong.edu.vn' trong kết quả tìm kiếm.")
    else:
        print("Trang đã tải xong. Bắt đầu cuộn trang mượt trong 120 giây...")
        start_time = time.time()
        while time.time() - start_time < 120:
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(0.5)
        print("Cuộn trang hoàn tất.")

# Hàm xử lý khi bấm nút Bắt đầu
def bat_dau():
    urls = [entry[0].get() for entry in url_entries if entry[0].get()]
    tu_khoas = [entry[0].get() for entry in tk_entries if entry[0].get()]

    if not urls or not tu_khoas:
        messagebox.showwarning("Lỗi", "Hãy nhập ít nhất một URL và một từ khóa.")
        return

    for url in urls:
        if not is_valid_url(url):
            messagebox.showerror("Lỗi URL", f"URL không hợp lệ: {url}")
            return

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        for tu_khoa in tu_khoas:
            for url in urls:
                driver.get(url)
                tim_kiem_va_cuon_trang(driver, tu_khoa)
    finally:
        driver.quit()

# Hàm thêm ô nhập URL mới
def them_url():
    entry = Entry(url_frame, width=40)
    entry.grid(row=len(url_entries), column=0, padx=5, pady=5)
    xoa_button = Button(url_frame, text="Xóa", command=lambda e=entry: xoa_entry(e, url_entries))
    xoa_button.grid(row=len(url_entries), column=1, padx=5, pady=5)
    url_entries.append((entry, xoa_button))

# Hàm thêm ô nhập từ khóa mới
def them_tu_khoa():
    entry = Entry(tk_frame, width=40)
    entry.grid(row=len(tk_entries), column=0, padx=5, pady=5)
    xoa_button = Button(tk_frame, text="Xóa", command=lambda e=entry: xoa_entry(e, tk_entries))
    xoa_button.grid(row=len(tk_entries), column=1, padx=5, pady=5)
    tk_entries.append((entry, xoa_button))

# Hàm xóa một ô nhập
def xoa_entry(entry, entry_list):
    entry_list.remove((entry, entry.winfo_manager()))
    entry.destroy()

# Tạo giao diện Tkinter
root = Tk()
root.title("Tìm kiếm và Cuộn trang")
root.geometry("600x400")

# Cột URL
Label(root, text="Nhập URL:").pack(anchor="w", padx=10)
url_frame = Frame(root)
url_frame.pack(fill="x", padx=10, pady=5)
url_entries = []
them_url_button = Button(root, text="Thêm URL", command=them_url)
them_url_button.pack(pady=5)

# Cột từ khóa
Label(root, text="Nhập từ khóa tìm kiếm:").pack(anchor="w", padx=10)
tk_frame = Frame(root)
tk_frame.pack(fill="x", padx=10, pady=5)
tk_entries = []
them_tk_button = Button(root, text="Thêm từ khóa", command=them_tu_khoa)
them_tk_button.pack(pady=5)

# Nút bắt đầu
bat_dau_button = Button(root, text="Bắt đầu", command=bat_dau)
bat_dau_button.pack(pady=20)

root.mainloop()
