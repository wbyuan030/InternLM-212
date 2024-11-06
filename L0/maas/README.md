# 玩转HF/Modelscope/Modelers
### 闯关任务
#### 模型下载
首先配置环境，并创建源文件,在codespace(https://github.com/codespaces)运行
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank $ touch hf_download_json.py
@wbyuan030 ➜ /workspaces/codespaces-blank $ pip install transformers==4.38
epiece==0.1.99
pip install einops==0.8.0
pip install protobuf==5.27.2
pip install accelerate==0.33.0Collecting transformers==4.38
```
后粘贴代码：
```python
import os
from huggingface_hub import hf_hub_download

# 指定模型标识符
repo_id = "internlm/internlm2_5-7b"

# 指定要下载的文件列表
files_to_download = [
    {"filename": "config.json"},
    {"filename": "model.safetensors.index.json"}
]

# 创建一个目录来存放下载的文件
local_dir = f"{repo_id.split('/')[1]}"
os.makedirs(local_dir, exist_ok=True)

# 遍历文件列表并下载每个文件
for file_info in files_to_download:
    file_path = hf_hub_download(
        repo_id=repo_id,
        filename=file_info["filename"],
        local_dir=local_dir
    )
    print(f"{file_info['filename']} file downloaded to: {file_path}")
```
如果本地下载，最好把hf endpoint 换成镜像站
```bash
export HF_ENDPOINT=https://hf-mirror.com
```
这对命令行工具 huggingface-cli 是有效的，python脚本下载没试过：）  
运行脚本
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank $ python hf_download_json.py 
```
下载飞快  
然后尝试一下codespace CPU推理：
首先看看规格
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank $ lscpu
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Byte Order:                         Little Endian
Address sizes:                      48 bits physical, 48 bits virtual
CPU(s):                             2
On-line CPU(s) list:                0,1
Thread(s) per core:                 2
Core(s) per socket:                 1
Socket(s):                          1
NUMA node(s):                       1
Vendor ID:                          AuthenticAMD
CPU family:                         25
Model:                              1
Model name:                         AMD EPYC 7763 64-Core Processor
Stepping:                           1
CPU MHz:                            3241.161
BogoMIPS:                           4890.86
Virtualization:                     AMD-V
Hypervisor vendor:                  Microsoft
Virtualization type:                full
L1d cache:                          32 KiB
L1i cache:                          32 KiB
L2 cache:                           512 KiB
L3 cache:                           32 MiB
```
分配的是二核四线的CPU  
粘贴代码
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("internlm/internlm2_5-1_8b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("internlm/internlm2_5-1_8b", torch_dtype=torch.float16, trust_remote_code=True)
model = model.eval()

inputs = tokenizer(["A beautiful flower"], return_tensors="pt")
gen_kwargs = {
    "max_length": 128,
    "top_p": 0.8,
    "temperature": 0.8,
    "do_sample": True,
    "repetition_penalty": 1.0
}

# 以下内容可选，如果解除注释等待一段时间后可以看到模型输出
output = model.generate(**inputs, **gen_kwargs)
output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
print(output)
```
执行脚本
```bash
python hf_1_8_demo.py
```
获得结果
```bash
A beautiful flower with a height of $3$ cm and a diameter of $2$ cm is placed on the table. A second flower, also of height $3$ cm, is placed on top of the first flower. The two flowers are in contact with each other, and the center of the second flower is $3$ cm above the center of the first flower. The radius of the first flower is $\frac{a}{b}$ , where $a$ and $b$ are relatively prime positive integers. Find $a+b$ .

Let $x$ be the distance from the bottom of the first flower to the
```

#### Space上传
https://huggingface.co/spaces/Hndsguy/colearn  
首先到huggingface创建一个space  
然后在codespace中clone这个space：
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank $ git lfs install
Git LFS initialized.
@wbyuan030 ➜ /workspaces/codespaces-blank $ git clone https://huggingface.co/spaces/<your name>/colearn
```
修改index为：
```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
  <title>My static Space</title>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    body {
      display: flex;
      justify-content: center;
      align-items: center;
    }
    iframe {
      width: 430px;
      height: 932px;
      border: none;
    }
  </style>
</head>
<body>
  <iframe src="https://colearn.intern-ai.org.cn/cobuild" title="description"></iframe>
</body>
</html>

```
然后推到云端  
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ git commit -a -m "add colearn static index"
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ git remote set-url origin https://<your name>:<your token>/spaces/<your name>/colearn
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ git push
```
这是用token access方式进行推送，也可以用SSH的方式，操作和GitHub类似  
最终效果：  
![alt text](image.png)

#### 模型上传  
最终仓库：  https://huggingface.co/Hndsguy/intern_study_L0_4/tree/main  

首先下载命令行工具
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ pip install huggingface_hub
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ git config --global credential.helper store
@wbyuan030 ➜ /workspaces/codespaces-blank/colearn (main) $ huggingface-cli login

    _|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|_|_|_|    _|_|      _|_|_|  _|_|_|_|
    _|    _|  _|    _|  _|        _|          _|    _|_|    _|  _|            _|        _|    _|  _|        _|
    _|_|_|_|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|  _|  _|_|      _|_|_|    _|_|_|_|  _|        _|_|_|
    _|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|  _|    _|      _|        _|    _|  _|        _|
    _|    _|    _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|        _|    _|    _|_|_|  _|_|_|_|

    To log in, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Enter your token (input will not be visible): 
Add token as git credential? (Y/n) y
Token is valid (permission: write).
The token `write_access` has been saved to /home/codespace/.cache/huggingface/stored_tokens
Your token has been saved in your configured git credential helpers (store).
Your token has been saved to /home/codespace/.cache/huggingface/token
Login successful.
The current active token is: `write_access`
```
>>git config --global credential.helper store意为存储账号信息，而不用每次和远程仓库交互都进行验证
创建项目仓库  
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank $ huggingface-cli repo create intern_study_L0_4
@wbyuan030 ➜ /workspaces/codespaces-blank $  git clone https://huggingface.co/Hndsguy/intern_study_L0_4
```
传入模型文件
```bash
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ cp ../internlm2_5-7b/config.json ./
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ git add /
fatal: /: '/' is outside repository at '/workspaces/codespaces-blank/intern_study_L0_4'
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ git add .
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ git commit -m "add config.json"
```
使用access token 验证并上传
```bash  
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ git remote set-url origin https://<your name>:<your token>@huggingface.co/<your name>/intern_study_L0_4/
@wbyuan030 ➜ /workspaces/codespaces-blank/intern_study_L0_4 (main) $ git push
```


