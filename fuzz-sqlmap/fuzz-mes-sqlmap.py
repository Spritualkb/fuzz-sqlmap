import os
import subprocess

def get_sqlmap_params(param_file):
    with open(param_file, 'r') as file:
        params = file.read().strip()
    return params

def run_sqlmap_on_files(folder, param_file):
    # 获取sqlmap的其他参数
    sqlmap_params = get_sqlmap_params(param_file)
    
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            # 构造sqlmap命令
            command = f"python ../sqlmap/sqlmap.py -r {file_path} {sqlmap_params}"
            print(f"Running: {command}")
            try:
                # 执行sqlmap命令
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running sqlmap on {file_path}: {e}")
 
if __name__ == "__main__":
    # 设置文件夹路径和参数文件路径
    folder_path = 'mes-data'
    param_file_path = 'sqlmap-param.txt'
    # 运行sqlmap批量测试
    run_sqlmap_on_files(folder_path, param_file_path)
