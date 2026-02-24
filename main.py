import asyncio
import csv
import string
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# --- 設定區 ---
api_id = '你的_API_ID'
api_hash = '你的_API_HASH'
phone = '你的電話'
channel_id = '你的頻道連結或ID' # 例如 https://t.me/your_channel 或 -100xxxx
output_file = "channel_subscribers.csv"

client = TelegramClient(phone, api_id, api_hash)

async def main():
    await client.start()
    print("登入成功！")

    try:
        # 獲取頻道實體
        entity = await client.get_entity(channel_id)
        print(f"開始抓取頻道：{entity.title}")

        all_subscribers = {} # 使用 dict 以 user_id 為 key 來去重

        # 搜尋字元清單：a-z + 0-9
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
                    all_subscribers[user.id] = user # 存入 dict 自動去重
                
                offset += len(participants.users)
                # 如果單次搜尋結果少於 limit，代表該關鍵字已搜完
                if len(participants.users) < limit:
                    break
                
                # 稍微停頓避免觸發 Rate Limit
                await asyncio.sleep(0.5)

        # 儲存結果
        print(f"抓取結束，總共獲得 {len(all_subscribers)} 個唯一訂閱者。")
        with open(output_file, "w", encoding='UTF-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User ID', 'Username', 'First Name', 'Last Name', 'Phone'])
            
            for user in all_subscribers.values():
                writer.writerow([
                    user.id, 
                    f"@{user.username}" if user.username else "",
                    user.first_name or "",
                    user.last_name or "",
                    user.phone or "Hidden"
                ])

        print(f"檔案已存至: {output_file}")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == '__main__':
    asyncio.run(main())