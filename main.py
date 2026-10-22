import requests
from bs4 import BeautifulSoup
import urllib3

# 停用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 填入步驟 1 取得的 Channel Access Token 與您的 User ID
LINE_ACCESS_TOKEN = "5d59d2a2146f66cd04686373b1a46c05"
USER_ID = "Ud44b7deb7227127613aba7357a63b643" 

def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("LINE 訊息發送成功！")
    else:
        print(f"發送失敗，HTTP 狀態碼: {response.status_code}, 回應: {response.text}")

def get_chiayi_work_school_status():
    url = "https://www.dgpa.gov.tw/typh/daily/nds.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"無法取得網頁資料，HTTP 狀態碼: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        chiayi_results = []
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            row_text = [col.text.strip() for col in cols]
            
            if row_text and any("嘉義市" in cell or "嘉義縣" in cell for cell in row_text):
                chiayi_results.append(" | ".join(row_text))

        # 組成發送訊息
        message = "📢【嘉義縣市 停班停課最新消息】\n\n"
        if chiayi_results:
            message += "\n".join(chiayi_results)
        else:
            message += "目前無停班停課訊息。"

        print(message)
        # 發送 LINE 推播訊息
        send_line_message(message)

    except Exception as e:
        print(f"抓取資料時發生錯誤: {e}")

if __name__ == "__main__":
    get_chiayi_work_school_status()

if chiayi_results:
    message = "📢【嘉義縣市 停班停課最新消息】\n\n" + "\n".join(chiayi_results)
    print(message)
    # 只有抓到停班停課時才發送 LINE 訊息
    send_line_message(message)
else:
    print("目前無停班停課訊息，不發送 LINE 通知。")
