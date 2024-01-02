# Flask web
your_project/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
│
├── app/
│   ├── adapters/          # Chứa các adapter (implementations) cho các cổng (gateways)
│   │   ├── controllers/
│   │   ├── database/
│   │   └── __init__.py
│   │
│   ├── core/              # Chứa các thành phần cốt lõi của ứng dụng
│   │   ├── entities/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── __init__.py
│   │
│   ├── interfaces/        # Chứa các giao diện (interfaces) cho các cổng (gateways)
│   │   ├── controllers/
│   │   ├── database/
│   │   └── __init__.py
│   │
│   ├── external/          # Chứa các thành phần giao tiếp với bên ngoài
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── config/                # Chứa các cấu hình ứng dụng
│   ├── __init__.py
│   └── config.py
│
├── migrations/            # Chứa các file migration cho cơ sở dữ liệu
│   └── __init__.py
│
├── tests/                 # Chứa các test cho ứng dụng
│   ├── unit/
│   ├── integration/
│   └── __init__.py
│
├── .env                   # File chứa các biến môi trường
├── .gitignore             # File chứa các đường dẫn không được theo dõi bởi Git
├── app.py                 # File chính khởi chạy ứng dụng
├── requirements.txt       # File chứa danh sách các thư viện cần cài đặt
└── README.md              # File mô tả dự án

Create virtual environment
> python -m venv venv
> venv\Scripts\activate

> pip install flask
