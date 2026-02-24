# Changelog

本專案的所有顯著變更將記錄在此檔案中。
格式參考自 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)。

## [1.0.0] - 2026-01

### Added
- **專案初始版本發佈**：實現基於 Telethon 框架的頻道成員抓取功能。
- **窮舉搜尋邏輯**：整合 `string.ascii_lowercase` 與 `digits`，透過 A-Z 與 0-9 的關鍵字迭代提升抓取覆蓋率。
- **自動去重系統**：引入 `all_subscribers` 字典機制，確保單次任務中 User ID 的唯一性。
- **CSV 匯出優化**：採用 `UTF-8-sig` 編碼格式，解決中文姓名在 Windows Excel 環境下的亂碼問題。
- **頻率控制**：在分頁抓取邏輯中加入 `asyncio.sleep` 間隔，提升程式運行穩定性。
- **異常處理機制**：加入 `try-except` 區塊，能捕捉並顯示執行過程中的 API 錯誤或連線問題。
- **欄位結構**：輸出的 CSV 包含 User ID、Username、First Name、Last Name 及 Phone。