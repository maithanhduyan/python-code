import os
import datetime
import configparser

# Lấy đường dẫn thư mục hiện tại
current_directory = os.getcwd()
print("Thư mục hiện tại:", current_directory)

# Lấy đường dẫn thư mục cha của thư mục hiện tại
parent_directory = os.path.dirname(current_directory)
print("Thư mục cha:", parent_directory)

# Tạo đường dẫn đến file backup.conf trong thư mục hiện tại
config_file_path = os.path.join(current_directory, 'backup.conf')
print("Thư mục backup:", config_file_path)

# Tạo đối tượng ConfigParser
config = configparser.ConfigParser()

# Đọc cấu hình từ file backup.conf
config.read(os.path.join(current_directory, 'backup.conf'))

directory_path = config.get('DownloadConfig', 'download_path')
print("Thư mục backup:", directory_path)

def get_list_of_file(directory_path):
    # Kiểm tra xem đường dẫn là một thư mục hợp lệ hay không
    if not os.path.isdir(directory_path):
        print("Đường dẫn không hợp lệ.")
        return

    # Lấy danh sách các tệp trong thư mục
    files = os.listdir(directory_path)

    # In tiêu đề của bảng
    print("{:<30} {:<15} {:<30}".format("Tên file", "Kích thước (MB)", "Ngày tạo"))

    for file_name in files:
        file_path = os.path.join(directory_path, file_name)

        # Kiểm tra xem đối tượng có phải là file hay không
        if os.path.isfile(file_path):
            # Lấy thông tin về file
            size = os.path.getsize(file_path)/1000000
            date_created = os.path.getctime(file_path)
            date_created_formatted = datetime.datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S')

            # In thông tin file ra màn hình
            print("{:<30} {:<15} {:<30}".format(file_name, size, date_created_formatted))

# Thay đổi đường dẫn thư mục cần kiểm tra tại đây
directory_path = config.get('DownloadConfig', 'download_path')
            
get_list_of_file(directory_path)