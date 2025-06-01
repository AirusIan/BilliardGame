# BilliardGame
BilliardGame 是一款簡易的網頁應用程式，設計目的是讓使用者可以自由安排撞球比賽時間，並在比賽結束後更新雙方排名。該系統最初作為實驗室內部活動專案，提升團隊互動與比賽透明度。

---

## 📌 專案簡介

- 🗓️ 比賽預約功能：由玩家自由發起並選擇對手
- 🎫 裁判登入與成績登錄機制
- 🧾 雙方比賽紀錄查詢
- 🏆 排行榜自動更新
- 🔐 使用者驗證（JWT）
- ☁️ 雲端部署（GCP + Cloud SQL）

---

## 🖼️ 系統架構圖

![image](https://github.com/user-attachments/assets/621d6a6e-17ce-4946-8333-5cd697523a6e)

---
## 🔁 系統流程說明

1. 使用者透過 **Register Page** 註冊帳號
2. 登入後導向 **Home Page**，依身分進行分流：
   - 玩家透過 JWT 登入，進入 **Personal Page**
   - 裁判登入後進入 **Ref Page**
3. 玩家可：
   - 在 **Race Page** 預約比賽
   - 查詢個人紀錄與排名
4. 裁判可：
   - 在 **Ref Page** 選擇比賽場次
   - 進入 **Register_result Page** 登錄比賽結果
5. 所有資料由 **Google Cloud SQL** 儲存，後端由 GCP 託管

---

## 🔧 使用技術總覽

| 類別       | 技術與工具說明                                  |
|------------|--------------------------------------------------|
| 📱 前端     | HTML + CSS     |
| 🧠 後端     | Flask / FastAPI，提供 RESTful API 與 JWT 驗證   |
| 🛢️ 資料庫   | Google Cloud SQL（PostgreSQL）         |
| 🔐 認證機制 | JSON Web Token (JWT)  |
| ☁️ 雲端平台 | Google Cloud Platform（GCP）、Cloud SQL|


以下為一些實際使用畫面
![image](https://github.com/user-attachments/assets/9e3edc4f-e77b-4625-8775-db1773f5bce7)
![image](https://github.com/user-attachments/assets/88356a0f-4f94-414d-9476-c9cb0b0bdb12)
![image](https://github.com/user-attachments/assets/88917fbb-4c62-4285-a330-8826b735f8b7)
![image](https://github.com/user-attachments/assets/0ca7c65c-9e2b-4770-be82-632a79aebe08)
![image](https://github.com/user-attachments/assets/999f6329-268b-42d5-b834-69f828201c86)
![image](https://github.com/user-attachments/assets/67b57d1a-817b-4b92-9df7-62614ea1dd49)

前端為HTML + CSS + JavaScript
後端為Django + CloudSQL並部屬至GCP
![image](https://github.com/user-attachments/assets/173dccd0-5326-47ed-96e3-b053e1a1d879)

User 登入有特別做JWT驗證
![image](https://github.com/user-attachments/assets/edf57aff-f285-4dfc-8406-feca495890ba)





