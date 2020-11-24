# 中国石油大学（华东）校园网络认证脚本

使用 Python 进行网络认证

## 源码依赖

使用 Python3 编写，依赖于

```
requests
urllib/urllib.parse
```

## 使用方法

### UPCNet.py

复制 `config.example.json` 并重命名为 `config.json`，修改 `config.json` 中的内容，执行 `UPCNet.py` 即可。 

#### config.json

```json
{
  "username": "your_school_number",
  "password": "your_password",
  "carrier": "your_carrier"
}
```

#### 不同运营商对应的 carrier 的值

| 运营商 | `carrier` 字段的值 |
| :---: | :---: |
| 校园网 | `default` |
| 联通 | `unicom` |
| 移动 | `cmcc` |
| 电信 | `ctcc` |
| 校园内网 | `local` |

## 部署

### Windows 可执行文件

> 需自行借助计划任务实现自动轮询

[github.com/LucienShui/UPCNet/releases](https://github.com/LucienShui/UPCNet/releases)

### Linux

> 每 5 分钟尝试连接一次校园网

首先克隆本项目至本地

```bash
git clone https://github.com/LucienShui/UPCNet.git /usr/local/upcnet
```

配置文件的位置为 `/usr/local/upcnet/config.json`

执行 `crontab -e` 之后，追加一行
 
```plain
*/5 * * * * (cd /usr/local/upcnet && exec /usr/bin/env python3 /usr/local/upcnet/UPCNet.py)
```

## 目前支持的网络类型：

理论上支持所有锐捷 `eportal` 认证。

## 版权信息

Author: [EndangeredFish](https://github.com/EndangeredF1sh)

Refactor: [LucienShui](https://github.com/LucienShui)
