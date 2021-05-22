# Jinmu cip (Check IP)

## 0. 说明

通常情况下的文字是描述, 在方框中的文字是终端中运行的命令. 不知道终端是啥? Google 一下?

``` zsh
# 框框里面的都是命令
# 不过 # 开头的都是注释, 可以不用复制, 复制了也没用
```

## 1. cip (zsh)

### 1.0 依赖第三方命令

cip 中使用了以下第三方命令:

- dig
- curl

### 1.1 Unix (Linux, macOS)

1. 放置在 __存在于系统环境变量的__ 的目录中, 例如:
    - /usr/local/bin/
    - /usr/bin/
    - ~/.bin/ (推荐, 建议创建该目录后将其添加至 环境变量:PATH 中, 并将后续个人安装的其他命令行工具和自定义命令都放置于该文件夹中)
2. 通过以下命令给 cip 文件通过 chmod 命令添加执行权限:

    ``` zsh
    chmod +x cip
    ```

3. cip用法如下:
    - cip IP
    - cip -f 包含ip列表的源文件 结果输出文件

## 2. cip.py (Python)

### 2.0 依赖第三方库

- requests
- dnspython

### 2.1 Unix (Linux, MacOS)

1. 将 cip.py 文件放置在一个 __自己能找得到__ 的目录中:
    1. 通过 Jinmu GitLab:
       1. 既然已经能看到这个 README 了, 那肯定是已经知道 git 怎么用了, git clone一下到本地吧
    2. 通过 dls.jinmu.info 下载:
       1. 下载链接: <https://dls.jinmu.info/iplocation/jm_akamai_cip/cip.py>
2. 安装 Python3.8+ (官网 <https://www.python.org>, 安装方法自行搜索);
3. pypi官方源速度慢的令人发指, 所以需要一个访问速度快的国内镜像源(可以理解成CDN).
    通过以下命令, 为 Python PIP 配置 清华大学 镜像源:

    ``` zsh
    python3 -m pip install pip -U
    python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    ```

    参考链接: <https://mirrors.tuna.tsinghua.edu.cn/help/pypi/>
4. 通过以下命令，为 Python 安装第三方库 requests, dnspython:

    ``` zsh
    python3 -m pip install requests dnspython
    ```

5. 为 cip 配置别名.
   以我的环境为例, 使用了zsh, 环境变量在 ~/.zshrc 中, cip文件的路径是 /Users/shengjyerao/git/jm_akamai_cip/cip.py，在 ~/.zshrc 中添加如下行

    ``` zsh
    alias cip="python3 /Users/shengjyerao/git/jm_akamai_cip/cip.py"
    ```

6. 查看 cip 版本以检查配置是否正常:

    ``` zsh
    cip -v
    ```

7. cip Python版本用法: cip (-h, --help 可不输入, 缺省参数时默认输出帮助) 查看帮助

### 2.2 Windows

1. 参考 2.1 Unix(Linux, MacOS) 中的步骤 1-2 完成脚本下载和python安装;
2. 在给 Windows Python pip 配置镜像源时，Python的命令不是 python3, 而是 python:

    ``` zsh
    python -m pip install pip -U
    python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    ```

3. 打开 PowerShell, 通过以下命令查看 PowerShell 配置文件路径:

    ``` PowerShell
    echo $PROFILE
    ```

    输出:

    ``` PowerShell
    C:\Users\shengjyerao\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    ```

    这是输出只是指明 PowerShell 通过读取这个文件的内容来加载自定义的内容，并不代表这个文件一定存在，所以应该把自定义配置信息写在这个文件里面，当这个文件不存在的时候需要手动创建。

4. 以文件路径 "C:\Users\shengjyerao\git\jm_akamai_cip\cip.py" 为例。
   通过vscode打开上面获取到的 PowerShell 配置文件, 添加以下内容并保存:

    ``` PowerShell
    function cip {
        python.exe C:\Users\shengjyerao\git\jm_akamai_cip\cip.py $args
    }
    ```

5. 关闭并重新打开 PowerShell, 检查 cip 命令是否正常

    ``` PowerShell
    cip -v
    ```
