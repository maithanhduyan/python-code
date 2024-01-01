import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
from datetime import datetime
import logging
from mail_manager import send_email
import configparser

# Lấy đường dẫn thư mục hiện tại
current_directory = os.getcwd()
print("Thư mục hiện tại:", current_directory)

# Tạo đối tượng ConfigParser
config = configparser.ConfigParser()

# Đọc cấu hình từ file backup.conf
config.read('backup.conf')

# Thông tin cấu hình email
email_config = {
    'subject': '',
    'html_body': '',
    'status_message' : '',
    'to_address': config.get('EmailConfig', 'to_address'),
    'smtp_server':  config.get('EmailConfig', 'smtp_server'),
    'smtp_port': config.getint('EmailConfig', 'smtp_port'),
    'smtp_username': config.get('EmailConfig', 'smtp_username'),
    'smtp_password': config.get('EmailConfig', 'smtp_password')
}

# Thư mục lưu log file
log_file_path = config.get('LoggingConfig', r'log_file_path')

# Thiết lập cấu hình logging
logging.basicConfig(filename=log_file_path , level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Đặt đường dẫn thư mục download
download_path = config.get('DownloadConfig', r'download_path')
chrome_options = webdriver.ChromeOptions()
prefs = {f'download.default_directory': download_path}
chrome_options.add_experimental_option('prefs', prefs)

# url
__url =config.get('BackupConfig','url')

# password
__password = config.get('BackupConfig','password')

def odoo_backup():
    """
        Automation click on web and fill password to backup odoo
    """
    try:
        # Khởi tạo Chrome WebDriver với các tùy chọn đã thiết lập
        driver = webdriver.Chrome(options=chrome_options)

        # Mở trang Odoo
        driver.get(__url)

        # Chờ để đảm bảo trang web đã được tải hoàn toàn
        time.sleep(1)

        # Nhấn nút "Backup" (hoặc tìm phần tử cần thiết)
        driver.find_element(By.XPATH, "//button[@data-db='taya_db']").click()

        # Chờ để đảm bảo trang web đã được tải hoàn toàn
        time.sleep(5)

        # Tìm trường password điền vào
        pwd_tag = driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div/div/form/div[1]/div[2]/div/div/input")
        pwd_tag.clear()
        pwd_tag.send_keys(__password)

        submit_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div/div/form/div[2]/input")
        submit_button.click()

        # Chờ để đảm bảo trang web đã được tải hoàn toàn
        time.sleep(10)

        # Ghi log khi backup thành công
        logging.info("Backup successfully completed.")

        # Send mail
        email_config.update({
            'subject':'Backup Successfully.',
            'status_message':'Backup Successfully',
        })
        send_email(**email_config)
        logging.info("Send email completed.")

    except Exception as e:
        # Ghi log khi có lỗi trong quá trình backup
        logging.error("Error during backup: %s", str(e))

        # Send mail when backup fail
        email_config.update({
            'subject':'Backup Fail.'.join(str(e)),
            'status_message':'Backup Fail',
        })
        send_email(**email_config)

    finally:
        # Đóng trình duyệt
        driver.quit()

def schedule_backup():
    logging.info("Running Odoo Backup.")
    odoo_backup()
    logging.info("Odoo Successful.")

if __name__ == "__main__":
    print(datetime.now(), "Running Odoo backup ...")
    logging.info("Running Odoo backup... ")
    # Tạo công việc chạy backup mỗi tuần vào Chủ nhật lúc 0 giờ
    schedule.every().sunday.at("00:00").do(schedule_backup)
    
    # Loop : Vòng lặp chạy tác vụ
    while True:
        schedule.run_pending()
        time.sleep(5)
