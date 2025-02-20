# Simple Blog API
繁體中文 | [English](./README-en.md)

基於 FastAPI 的簡易部落格後端 API。

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
- `POST /login`：使用者登入。參數為 `email` 和 `password`，分別為使用者帳號和密碼。登入成功後會回傳一個效期 30 天的 JWT，欄位包含使用者 Email 、 憑證之 Issuer 、 Expiration Time 、 Not Before。

### blog
- `GET /blog/all`：列舉所有文章（標題、內文、標籤）。
- `GET /blog/page/{page}`：列舉分頁文章（標題、內文、標籤）。參數為 `pagesize`，非必填，用於設定每頁文章數，預設值為 10。
- `POST /blog/create`：新增文章。會驗證 JWT，若驗證失敗將回傳 401 狀態。 Request 攜帶之 data 需為 JSON，當中包含 `title` （字串）、`content` （字串） 和 `tags` （陣列，元素為字串），分別為文章之標題、內文和標籤。

## 運行服務
### 本地端
#### 環境需求
* Python 3.10+
* MySQL 8.0+

#### FastAPI
1. 安裝依賴
```bash
pip install -r requirements.txt
```
2. 啟動應用
```bash
uvicorn app:app --reload
```
後端啟動後，API 服務將運行於 [http://127.0.0.1:8000](http://127.0.0.1:8000)，並可透過 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看 Swagger UI 文件。

#### MySQL
1. 打開 MySQL Command Line 並登入。
2. 執行 SQL Script。
```bash
source D://Simple-Blog-API/sql/init.sql
```
> 註：`D://Simple-Blog-API/sql/init.sql` 應替換為 `init.sql` 實際的絕對路徑。

### Docker
啟動 Docker Compose 容器。
```bash
docker compose up -d --build
```
應用啟動後：
* API 服務將運行於 [http://localhost:8000](http://localhost:8000)，並可透過 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 Swagger UI 文件。
* MySQL 服務將運行於 [http://localhost:3307](http://localhost:3307)。

## 環境變數
本服務需定義如下環境變數：
- `DATABASE_URL`：MySQL 資料庫連線字串。
- `JWT_ISSUER`：JWT 發行者（可選，如未設定則預設為`fastapi`）。
- `SECRET_KEY`：JWT 秘鑰（可選，如未設定則啟動服務時將自動產生）。

### 於本地端運行服務
請將 `.env.template` 檔案複製為 `.env` 檔案，並在 `.env` 檔案中修改上述環境變數值。

### 以 Docker 運行服務
請於 `docker-compose.yml` 檔案中，在 `app` 的 `environment` 欄位修改上述環境變數值。其中 `DATABASE_URL` 已經設定，如無必要，建議不要修改以免 API 服務無法連接資料庫。
