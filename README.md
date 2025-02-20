# Simple Blog API

## 架構
```
blog-api/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   └── login.py
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── sql/
│   └── init.sql
├── .dockerignore
├── .env.template
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

## API 說明
### login
- `POST /login`: 使用者登入。登入成功後會回傳 JWT。

### blog
- `GET /blog/all`: 取得所有文章。
- `GET /blog/page/{page}`: 取得分頁文章。可攜帶 `pagesize` 參數設定每頁文章數，預設值為 10。
- `POST /blog/create`: 新增文章。會驗證 JWT，若驗證失敗將回傳 401 狀態。

## 運行服務
### 本地端
#### FastAPI
1. 安裝依賴
```bash
pip install -r requirements.txt
```
2. 啟動應用
```bash
uvicorn main:app --reload
```
後端啟動後，API 服務將運行於 [http://127.0.0.1:8000](http://127.0.0.1:8000)，並可透過 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看 Swagger UI 文件。

#### MySQL
```bash
mysql -u root -p < sql/init.sql
```

### Docker
啟動 Docker Compose 容器。
```bash
docker compose up -d --build
```
後端啟動後，API 服務將運行於 [http://localhost:8000](http://localhost:8000)，並可透過 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 Swagger UI 文件。

## 環境變數
本服務需定義如下環境變數：
- `DATABASE_URL`：MySQL 資料庫連接字串。
- `JWT_ISSUER`：JWT 發行者，如未設定則預設為`fastapi`。
- `SECRET_KEY`：JWT 秘鑰，如未設定則啟動服務時將自動產生。

### 於本地端運行服務
請將 `.env.template` 檔案複製為 `.env` 檔案，並在 `.env` 檔案中修改上述環境變數值。

### 以 Docker 運行服務
請於 `docker-compose.yml` 檔案中，在 `app` 的 `environment` 欄位修改上述環境變數值。其中 `DATABASE_URL` 已經設定，如無必要，建議不要修改。
