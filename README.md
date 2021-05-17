# Jinmu cip (Check IP)

## 1. cip (Shell)

### 1.1 Unix (Linux, MacOS)

1. 放置在 __存在于系统环境变量的__ 的目录中, 例如:
    - /usr/local/bin/
    - /usr/bin/
    - ~/.bin/ (推荐, 建议创建该目录后将其添加至 环境变量:PATH 中, 并将后续个人安装的其他命令行工具和自定义命令都放置于该文件夹中)
2. 给 cip 文件通过 chmod 命令添加执行权限:

    ``` zsh
    chmod +x cip
    ```

3. cip用法如下:
    1. cip IP
    2. cip -f 包含ip列表的源文件 结果输出文件

## 2. cip.py (Python)

### 2.1 Unix (Linux, MacOS)

1. 将 cip.py 文件放置在一个 __自己能找得到__ 的目录中;
2. 安装 Python3.8+ (官网 <https://www.python.org>, 安装方法自行搜索);
3. 为 Python PIP 配置 清华大学 镜像源;
    <https://mirrors.tuna.tsinghua.edu.cn/help/pypi/>
4. 为 Python 安装第三方库 requests, dnspython:

    ``` zsh
    python3 -m pip install requests, dnspython
    ```

5. 在环境变量中, 为 cip配置别名, 以我的环境为例:

    ``` zsh
    alias cip="python3 /Users/shengjyerao/git/jm_akamai_cip/cip.py"
    ```

6. 查看 cip 版本以检查配置是否正常:

    ``` zsh
    cip -v
    ```

7. cip Python版本用法: cip (-h, 可不输入, 缺省参数时默认输出帮助) 查看帮助

### 2.2 Windows

1. 以文件路径 "C:\Users\shengjyerao\git\jm_akamai_cip\cip.py" 为例, 按照 2.1 Unix(Linux, MacOS) 中完成步骤 1 - 4;
2. 打开 PowerShell, 使用查看 PowerShell 配置文件路径:

    ``` PowerShell
    echo $PROFILE
    ```

    输出:

    ``` PowerShell
    C:\Users\shengjyerao\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    ```

3. 打开 PowerShell 配置文件, 添加以下内容:

    ``` PowerShell
    function cip {
        python.exe C:\Users\shengjyerao\git\jm_akamai_cip\cip.py $args
    }
    ```

4. 关闭并重新打开 PowerShell, 检查 cip 命令是否正常

    ``` PowerShell
    cip -v
    ```
