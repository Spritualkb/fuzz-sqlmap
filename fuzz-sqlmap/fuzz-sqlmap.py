import os
import subprocess
import concurrent.futures

def run_sqlmap_command(command):
    """在新的 CMD 窗口中执行 sqlmap 命令，并等待完成"""
    # 使用 subprocess 启动一个新的 CMD 窗口执行命令
    process = subprocess.Popen(command, shell=True)
    process.wait()  # 等待该进程完成
    return process.returncode

def main():
    print("""
  .--.--.                                 ___                                ,--,         ,-.            
 /  /    '. ,-.----.             ,--,   ,--.'|_                            ,--.'|     ,--/ /|   ,---,    
|  :  /`. / \    /  \   __  ,-.,--.'|   |  | :,'          ,--,             |  | :   ,--. :/ | ,---.'|    
;  |  |--`  |   :    |,' ,'/ /||  |,    :  : ' :        ,'_ /|             :  : '   :  : ' /  |   | :    
|  :  ;_    |   | .\ :'  | |' |`--'_  .;__,'  /    .--. |  | :    ,--.--.  |  ' |   |  '  /   :   : :    
 \  \    `. .   : |: ||  |   ,',' ,'| |  |   |   ,'_ /| :  . |   /       \ '  | |   '  |  :   :     |,-. 
  `----.   \|   |  \ :'  :  /  '  | | :__,'| :   |  ' | |  . .  .--.  .-. ||  | :   |  |   \  |   : '  | 
  __ \  \  ||   : .  ||  | '   |  | :   '  : |__ |  | ' |  | |   \__\/: . .'  : |__ '  : |. \ |   |  / : 
 /  /`--'  /:     |`-';  : |   '  : |__ |  | '.'|:  | : ;  ; |   ," .--.; ||  | '.'||  | ' \ \'   : |: | 
'--'.     / :   : :   |  , ;   |  | '.'|;  :    ;'  :  `--'   \ /  /  ,.  |;  :    ;'  : |--' |   | '/ : 
  `--'---'  |   | :    ---'    ;  :    ;|  ,   / :  ,      .-./;  :   .'   \  ,   / ;  |,'    |   :    | 
            `---'.|            |  ,   /  ---`-'   `--`----'    |  ,     .-./---`-'  '--'      /    \  /  
              `---`             ---`-'                          `--`---'                      `-'----'   
""")


    print("""
*************************************
*         SQLMap 批量测试工具         *
*           作者: Spritualkb           *
*            版本: 1.0               *
*          描述:                   *
* 本脚本用于批量测试指定的URL是否存在SQL注入漏洞。*
* 如果urls.txt文件为空，脚本将从ip.txt文件读取IP地址，*
* 并结合ip-param.txt中的路径和参数构建URL进行测试。*
*************************************
""")

    # 文件路径定义
    urls_file = 'urls.txt'        # 存放待测试的URL列表文件
    sqlmap_param_file = 'sqlmap-param.txt'  # 存放传递给sqlmap的参数的文件
    post_data_file = 'postData.txt'        # 存放POST请求数据的文件
    headers_file = 'headers.txt'           # 存放HTTP请求头的文件
    ip_file = 'ip.txt'                    # 存放IP地址列表的文件
    ip_param_file = 'ip-param.txt'        # 存放路径和请求参数的文件

    # 读取sqlmap参数
    with open(sqlmap_param_file, 'r') as file:
        sqlmap_params = file.read().strip()  # 读取并去除参数中的多余空格

    # 读取POST数据
    post_data = ""
    if os.path.exists(post_data_file):
        with open(post_data_file, 'r') as file:
            post_data = file.read().strip()  # 读取并去除POST数据中的多余空格

    # 读取请求头
    headers = ""
    if os.path.exists(headers_file):
        with open(headers_file, 'r') as file:
            headers = file.read().strip()  # 读取并去除请求头中的多余空格

    # 读取并去重URL列表
    with open(urls_file, 'r') as file:
        urls = list(set(url.strip() for url in file if url.strip()))  # 清除多余的空格和换行符并去重

    # 如果urls.txt为空，从ip.txt和ip-param.txt获取信息
    if not urls:
        with open(ip_file, 'r') as file:
            ips = list(set(ip.strip() for ip in file if ip.strip()))  # 清除多余的空格和换行符并去重
        
        with open(ip_param_file, 'r') as file:
            ip_params = file.read().strip()  # 读取并去除路径和请求参数中的多余空格
        
        # 判断ip_params是否以斜杠开头，并根据情况构建URL
        urls = [f"http://{ip}{ip_params if ip_params.startswith('/') else '/' + ip_params}" for ip in ips]

    # 使用 ThreadPoolExecutor 来并发执行 sqlmap 命令
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            if not url:
                continue

            # 构建 sqlmap 命令
            command = f"start cmd /k python ../sqlmap/sqlmap.py -u \"{url}\""
            if post_data:
                command += f" --data \"{post_data}\""
            if headers:
                command += f" --headers \"{headers}\""
            command += f" {sqlmap_params}"

            # 向线程池提交任务
            futures.append(executor.submit(run_sqlmap_command, command))

        # 等待所有任务完成
        concurrent.futures.wait(futures)

    # 完成所有任务后退出主窗口
    print("所有任务完成。")
    os.system('pause')  # 这样主窗口将保持打开状态直到用户手动关闭

if __name__ == '__main__':
    main()
