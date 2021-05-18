# encoding=utf-8

"""
cip(Check IP) 的 Python3 版本
"""


import argparse
import os
import re
import sys

import dns.resolver
import requests

# cip 版本信息
__version__ = "0.1.2"
cip_info_version = """
版本: {0}
时间: 2021-05-18 11:13:05"
编辑: aojie654"
邮箱: shengjie.ao@jinmuinfo.com
""".format(__version__)

# 版本日志
log_version = """
v 0.1.1:
简介:
- 无
功能更新:
- 增加了更新日志
- 为版本更新时的输出增加换行, 并输出更新日志
- 更新了版本信息显示方式
- 更新了版本号 ╮(￣▽￣)╭

v 0.1.0:
简介:
- cip Python 版的第一个版本
功能更新:
- 支持多 IP/域名/文件 输入
- 支持 非本地DNS
- 增加了较为友好的帮助功能
- 增加了较为便捷的更新功能
"""

# 定义cip服务器信息, DNS
server_cip = "cip.jinmu.info"
server_dns = str()


def cip_direct(input_tmp):
    """
    cip 输入为直接输入IP或域名时的处理流程
    """

    # 根据输入获取cip结果列表
    result_cip_list = cip_process(input_tmp)

    # 将列表中的元素依次输出
    for result_cip in result_cip_list:
        print(result_cip)

    return


def cip_file(file_list_tmp):
    """
    cip 输入为文件时的处理流程
    """
    # 若输入包含 -f 参数, 则输入为文件列表
    for file_tmp in file_list_tmp:
        # 获取 内容列表
        file_content_list = file_reader(file_tmp)
        # 当列表长度不为0时, 将文件内容列表作为输入调用cip_process, 获取结果后写入文件
        if len(file_content_list) != 0:
            result_cip_file = cip_process(input_tmp=file_content_list)
            file_writer(file_tmp=file_tmp, content_list_tmp=result_cip_file)
        else:
            pass

    return


def cip_process(input_tmp):
    """
    cip 的通用处理流程
    """

    # 初始化 cip结果列表
    result_cip_list = list()
    # 遍历列表中的每个元素
    for input_tmp in input_tmp:
        # 判断当前元素中的类型
        ioh_type = judge_input(input_tmp=input_tmp)
        if ((ioh_type == "ipv4") or (ioh_type == "ipv6")):
            # 当 ioh是 ipv4 或者 ipv6, 调用ip查询函数
            result_cip_list.append(cip_ip(ip_tmp=input_tmp))
        elif (ioh_type == "domain"):
            # 当 ioh 是 域名类型时, 调用域名查询函数
            result_cip_direct = cip_domain(domain_tmp=input_tmp)
            result_cip_list = result_cip_list + result_cip_direct
        else:
            # 不属于 ip或域名 时, 查询结果为错误提示
            result_cip_direct = "参数有误, {0} 非有效的ip或域名".format(input_tmp)
            result_cip_list.append(result_cip_direct)

    return result_cip_list


def file_reader(file_tmp):
    """
    根据文件读取内容并生成文件列表
    """

    file_content_list = list()
    # 当文件存在时读取文件内容
    if os.path.exists(file_tmp):
        # 打开文件, 读取内容后去掉尾部多余字符, 然后以回车分割
        file_object = open(file_tmp, encoding="utf-8", mode="r")
        file_content = file_object.read().rstrip()
        file_object.close()
        file_content_list = file_content.split("\n")
    else:
        # 文件不存在时输出提醒
        print("文件: {0} 不存在!".format(file_tmp))

    return file_content_list


def file_writer(file_tmp, content_list_tmp):
    """
    将传入的数组列表追加至文本后
    """

    # 以追加模式打开文件,
    file_object = open(file_tmp, encoding="utf-8", mode="a")
    # 添加空字符串 和 结果提示信息
    content_list_tmp = ["", "", "以上内容的查询结果如下:"] + content_list_tmp
    # 并将结果集中的内容依次添加回车后写入文件后关闭文件
    for content_tmp in content_list_tmp:
        file_object.writelines("{0}\n".format(content_tmp))
        file_object.flush()
    file_object.close()
    # 输出处理结果提示
    print("文件: {0} 内容查询已完成, 结果已追加至源文件内".format(file_tmp))

    return


def judge_input(input_tmp):
    """
    判断 对象类型
    """

    # 初始化 ipv4, ipv6, 域名的对应正则匹配表达式
    re_ipv4 = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    re_ipv6 = "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$"
    re_domain = "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$"

    # 根据正则匹配判断 ioh类型, 并 保存至 ioh_type
    ioh_type = "na"
    if re.match(re_ipv4, input_tmp):
        ioh_type = "ipv4"
    elif re.match(re_ipv6, input_tmp):
        ioh_type = "ipv6"
    elif re.match(re_domain, input_tmp):
        ioh_type = "domain"
    else:
        pass

    # 返回 ioh 类型
    return ioh_type


def cip_domain(domain_tmp):
    """
    Domain To Location 查询
    """

    # 获取域名对应解析的IP列表
    ip_list = domain_resolve(domain_tmp=domain_tmp)
    # 初始化域名对应IP查询结果列表
    cip_list_domain = list()
    # 初始化域名查询开始和结束信息
    domain_info = "{0:=^54}".format(domain_tmp)
    # 遍历ip列表, 调用cip_ip, 并将结果追加至结果列表
    cip_list_domain.append(domain_info)
    for ip_tmp in ip_list:
        result_cip_ip = cip_ip(ip_tmp=ip_tmp)
        cip_list_domain.append("{1}{0}".format(result_cip_ip, "=" * 2))
    cip_list_domain.append(domain_info)

    return cip_list_domain


def domain_resolve(domain_tmp):
    """
    域名解析
    """
    # 创建 resolver对象
    resolver_tmp = dns.resolver.Resolver()
    # 当DNS服务器不为空时, 使用传入的DNS服务器
    if server_dns != "":
        resolver_tmp.nameservers = server_dns
    else:
        pass
    # 初始化ip列表
    ip_list = list()
    # 将解析出的所有结果逐一添加到ip列表结果里
    for rrset_tmp in resolver_tmp.resolve(domain_tmp).rrset:
        if rrset_tmp.address != "":
            ip_list.append(rrset_tmp.address)

    return ip_list


def cip_ip(ip_tmp):
    """
    单个 IP To Location 查询
    """
    # 初始化 查询URL, 初始化一个空的结果字符串
    url_cip = "https://{0}/es?ip={1}".format(server_cip, ip_tmp)
    result_cip = requests.get(url_cip)
    result_cip_ip = str()

    # 当状态码为200时返回结果, 否则返回失败信息
    if result_cip.status_code == 200:
        result_cip_ip = result_cip.text
    else:
        result_cip_ip = "查询 {0} 失败, 状态码: {1}".format(ip_tmp, result_cip.status_code)

    return result_cip_ip


def get_version():
    """
    获取当前版本
    """

    result_version = cip_info_version

    return result_version


def check_update():
    """
    检查脚本更新
    """
    # 初始化 cip更新服务器 及 url
    server_update = "dls.jinmu.info"
    url_cip_file = "https://{0}/iplocation/cip.py".format(server_update)
    url_cip_version = "https://{0}/iplocation/cip.version".format(server_update)
    # 创建对象获取远端版本
    result_request_cip_version = requests.get(url_cip_version)
    # 当状态码存在且为200时:
    if ((result_request_cip_version.status_code is not None) and (result_request_cip_version.status_code == 200)):
        # 获取版本信息内容并去除末尾回车, 输出更新信息
        result_remote = result_request_cip_version.text.rstrip()
        update_info = "cip 更新 URL 为: {0}\n文件路径为: {1}\n当前版本为: {2}\ncip 远端版本为: {3}, ".format(url_cip_file, __file__, __version__, result_remote)
        print(update_info)
        if result_remote > __version__:
            # 当远端版本高于当前版本时, 进行文件更新
            result_request_cip_file = requests.get(url_cip_file)
            if ((result_request_cip_file.status_code is not None) and (result_request_cip_file.status_code == 200)):
                # 文件请求状态正常时, 输出更新开始状态
                print("请求远端cip文件正常, 开始更新...")
                # 定义 cip文件 的路径
                path_file_cip = __file__
                # 将远程文件的内容写入 临时文件中
                object_cip_file = open(file=path_file_cip, encoding="utf-8", mode="w", errors="ignore")
                object_cip_file.write(result_request_cip_file.text)
                object_cip_file.flush()
                object_cip_file.close()
                # 输出更新日志
                log_version = get_log_version()
                print(log_version)
                # 输出更新完成状态
                print("更新完成啦, 看看写代码的这次又新增了多少个bug *~(￣▽￣)~*")
            elif (result_request_cip_file.status_code is not None):
                print("请求远端cip文件出错! 未收到请求响应码")
            else:
                print("请求远端cip文件出错! 响应码: {0}".format(result_request_cip_file.status_code))
        elif result_remote == __version__:
            # 版本一致时提示无需更新
            print("和远端版本一样咯, 没必要更新啦 *~(￣▽￣)~*")
        else:
            # 远端版本低于当前版本时
            print("怕不是写代码的又偷懒了, 请喊他更新远端版本 *~(￣▽￣)~*")
    elif (result_request_cip_version.status_code is None):
        print("获取远端版本出错! 未收到请求响应码!")
    else:
        print("获取远端版本出错! 状态码为: {0}".format(result_request_cip_version.status_code))

def get_log_version():
    """
    返回 版本日志
    """

    return log_version

if __name__ == "__main__":
    # 创建 参数解析对象
    parser = argparse.ArgumentParser(
        prog="cip",
        description="将传入的 IP 或者域名通过 Akamai Edgescape 转化为地理位置信息",
    )

    # 添加 ioh, dns, 文件 及 更新参数
    parser.add_argument("input", nargs="+", help="输入, 默认为 IP 或域名, 可输入多个")
    # parser.add_argument("update", help="显示 当前文件版本及更新URL", action="store_true")
    parser.add_argument("-d", "--dns", nargs="+", help="在输入域名时指定 DNS服务器, 未指定时默认使用 Local DNS")
    # parser.add_argument("-h", "--help", help="显示该帮助文本后退出", dest="", action="store_true")
    parser.add_argument("-f", "--file", help="以文件作为输入, 并将结果追加至文件内", action="store_true")
    parser.add_argument("-l", "--log", help="查看更新日志", action="store_true")
    parser.add_argument("-u", "--update", help="更新cip", action="store_true")
    parser.add_argument("-v", "--version", help="查看当前文件版本信息", action="store_true")
    # 解析参数

    # sys.argv = ("1.1.1.1 www.baidu.com 1.11.1.2 x")
    # sys.argv = ("1.1.1.1 www.baidu.com 1.11.1.2 x -d 1.1.1.1 1.1.1.2 8.8.8.8 8.8.4.4")
    # sys.argv = ("-f 1.txt /Users/shengjyerao/Downloads/iptest.txt")
    # sys.argv = ("-f 1.txt /Users/shengjyerao/Downloads/iptest.txt -d 1.1.1.1 1.1.1.2 8.8.8.8 8.8.4.4")
    # sys.argv = (__file__ + " -v")
    # sys.argv = (__file__ + " -u")

    if len(sys.argv) == 1:
        # 当传入参数长度为1, 即未指定任何参数时, 默认输出帮助
        parser.print_help()
    elif ("-l" or "--log") in sys.argv:
        # 当参数中包含 -u 或者 --update 的时候检查更新
        print(get_log_version())
    elif ("-u" or "--update") in sys.argv:
        # 当参数中包含 -u 或者 --update 的时候检查更新
        check_update()
    elif ("-v") in sys.argv:
        # 当参数中包含 -v 或者 --version 的时候检查更新
        print(get_version())
    elif("--version") in sys.argv:
        # 只输出版本信息
        print(__version__)
    else:
        # 显示运行开始提示
        print("{0:=^50}".format(" cip运行开始 "))
        args = parser.parse_args()

        # 使用输入时指定的dns服务器
        if args.dns:
            # 当DNS服务器不为空时, 使用传入的DNS服务器
            server_dns = args.dns
            info_dns = " 当前使用的DNS服务器为: {0} ".format(server_dns)
            print("{0:=^45}".format(info_dns))
        else:
            print("{0:=^47}".format(" 使用本地DNS服务器 "))

        # 判断输入的类型是否为文件
        if not args.file:
            # 如果 -f 不存在, 将 ip或域名 作为输入为调用 cip
            cip_direct(input_tmp=args.input)
        else:
            # 存在 -f 时, 将 文件列表 作为输入调用 cip_file
            cip_file(file_list_tmp=args.input)
        # 显示运行结束提示
        print("{0:=^50}".format(" cip运行结束 "))
