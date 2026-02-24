import asyncio
import csv
import string
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent

# --- 設定區 ---
api_id = '12345678'  # 請替換為你的 API ID
api_hash = 'abcdef1234567890abcdef1234567890'  # 請替換為你的 API Hash
phone = '+886123456789'  # 請替換為你的電話號碼
channel_id = 'https://t.me/yourchannel'  # 請替換為你要抓取的頻道連結或ID
output_file = "channel_subscribers.csv"

client = TelegramClient(phone, api_id, api_hash)

async def main():
    await client.start()
    print("登入成功！")

    try:
        # 獲取頻道實體
        entity = await client.get_entity(channel_id)
        print(f"開始抓取頻道：{entity.title}")

        all_subscribers = {} # 使用 dict 以 user_id 為 key，重複加入會自動覆蓋（即去重）

        # --- 步驟 1：抓取最近加入的 200 人 ---
        print("正在抓取最近加入的 200 位成員...")
        recent_participants = await client(GetParticipantsRequest(
            channel=entity,
            filter=ChannelParticipantsRecent(),
            offset=0,
            limit=200,
            hash=0
        ))
        
        for user in recent_participants.users:
            all_subscribers[user.id] = user
        print(f"目前已收集 (含最近成員): {len(all_subscribers)} 人")

        # --- 步驟 2：執行關鍵字搜尋抓取 (A-Z, 0-9) ---
        search_queries = string.ascii_lowercase + string.digits

        for query in search_queries:
            offset = 0
            limit = 100
            print(f"正在搜尋關鍵字：'{query}'...")
            
            while True:
                participants = await client(GetParticipantsRequest(
                    channel=entity,
                    filter=ChannelParticipantsSearch(query),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))
                
                if not participants.users:
                    break
                
                for user in participants.users:
                    # 如果 ID 已存在，dict 會自動處理，不會重複增加數量
                    all_subscribers[user.id] = user 
                
                offset += len(participants.users)
                if len(participants.users) < limit:
                    break
                
                await asyncio.sleep(0.5)

        # --- 步驟 3：儲存結果 ---
        print(f"抓取結束，總共獲得 {len(all_subscribers)} 個唯一訂閱者。")
        
        with open(output_file, "w", encoding='UTF-8-sig', newline='') as f:
            writer = csv.writer(f)
            # 修正標題欄位，使其與內容對應
            writer.writerow(['User ID', 'Username', 'First Name', 'Last Name', 'Phone'])
            
            for user in all_subscribers.values():
                writer.writerow([
                    user.id, 
                    f"@{user.username}" if user.username else "", # 確保帳號帶有 @
                    user.first_name or "",
                    user.last_name or "",
                    user.phone or "Hidden"
                ])

        print(f"檔案已成功存至: {output_file}")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == '__main__':
    asyncio.run(main())