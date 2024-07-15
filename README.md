## SQLMap 批量测试工具

### 概述

SQLMap 批量测试工具是一款用于批量测试指定的 URL 或包含 HTTP 请求的文件是否存在 SQL 注入漏洞的脚本工具。工具提供两种主要功能：通过 URL 列表进行测试和通过文件夹中的 HTTP 请求文件进行测试。

### 功能

- 读取 URL 列表并进行 SQL 注入漏洞测试。
- 读取包含 HTTP 请求的文件并进行 SQL 注入漏洞测试。
- 支持自定义 SQLMap 参数、POST 请求数据和 HTTP 请求头。
- 自动遍历指定文件夹中的所有文件并进行测试。

### 目录结构

```
E:\BaiduSyncdisk\Notebook\easy-hack-tools\fuzz-sqlmap
|-- fuzz-mes-sqlmap.py                # 第二个主脚本文件
|-- fuzz-sqlmap.py                    # 第一个主脚本文件
|-- headers.txt                       # 存放 HTTP 请求头
|-- ip.txt                            # 存放 IP 地址列表
|-- ip-param.txt                      # 存放路径和请求参数
|-- mes-data/                         # 存放包含 HTTP 请求的文件
|-- postData.txt                      # 存放 POST 请求数据
|-- README.md                         # 说明文档
|-- sql_time_inject.py                # 其他 SQL 注入脚本
|-- sqlmap-param.txt                  # 存放传递给 SQLMap 的参数
|-- urls.txt                          # 存放待测试的 URL 列表
|-- yakit-output-1901544795-2024_06_19-03_09_53.csv  # 数据输出文件
|-- start fuzz-mes-sqlmap.bat         # 启动 fuzz-mes-sqlmap 脚本的批处理文件
|-- start fuzz-sqlmap.bat             # 启动 fuzz-sqlmap 脚本的批处理文件
```

### 使用说明

#### 第一个脚本 (`fuzz-sqlmap.py`)

1. **准备文件**

   - `urls.txt`: 将待测试的 URL 列表逐行写入该文件。
   - `sqlmap-param.txt`: 将需要传递给 SQLMap 的参数写入该文件。
   - `postData.txt` (可选): 如果需要进行 POST 请求测试，将 POST 数据写入该文件。
   - `headers.txt` (可选): 如果需要自定义 HTTP 请求头，将请求头写入该文件。
   - `ip.txt` 和 `ip-param.txt`: 如果 `urls.txt` 为空，将从 `ip.txt` 中读取 IP 地址，并结合 `ip-param.txt` 中的路径和参数构建 URL 进行测试。

2. **运行脚本** 打开命令行终端，进入脚本所在目录，执行以下命令：

   ```
   python fuzz-sqlmap.py
   ```

#### 第二个脚本 (`fuzz-mes-sqlmap.py`)

1. **准备文件夹和参数文件**

   - `mes-data/`: 将包含 HTTP 请求的文件放入该文件夹。
   - `sqlmap-param.txt`: 将需要传递给 SQLMap 的参数写入该文件。

2. **运行脚本** 打开命令行终端，进入脚本所在目录，执行以下命令：

   ```
   python fuzz-mes-sqlmap.py
   ```

### 示例

假设有以下文件内容：

- `sqlmap-param.txt`:

  ```
  --batch --level=5 --risk=3
  ```

- `mes-data/` 文件夹中包含多个 HTTP 请求文件，例如 `request1.txt`、`request2.txt` 等。

运行 `fuzz-mes-sqlmap.py` 脚本后，工具将遍历 `mes-data/` 文件夹中的所有文件，并使用 SQLMap 进行测试。

### 版权信息

作者: Spritualkb
版本: 1.0
描述: 本脚本用于批量测试指定的 URL 或包含 HTTP 请求的文件是否存在 SQL 注入漏洞。



