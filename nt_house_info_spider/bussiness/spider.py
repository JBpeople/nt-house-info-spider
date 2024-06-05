import queue
import re
import threading

import lxml
import lxml.etree
import requests

from nt_house_info_spider.db.house_info_table import HouseInfoTable
from nt_house_info_spider.log import logger
from nt_house_info_spider.static import constant


def get_pages_url() -> queue.Queue | None:
    """
    获取房源页面的url列表，并存入队列中返回

    Returns:
        Optional[Queue]: 包含房源页面url的队列，若获取总页数失败则返回None

    """
    url_queue: queue.Queue = queue.Queue()
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.107 Safari/537.36",
    }

    response = requests.get(constant.URL, headers=header)
    html = lxml.etree.HTML(response.text)
    res = html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')
    try:
        page_info = eval(res[0])
        page_num = page_info["totalPage"]
        logger.info(f"------> 获取总页数成功{page_num}")
    except IndexError:
        logger.error("-----> 获取总页数失败")
        return None
    for i in range(1, page_num + 1):
        url = constant.URL + f"pg{i}/"
        url_queue.put(url)
    return url_queue


def parse_house_info(house_info: str) -> list:
    """
    从房屋信息字符串中解析出楼层、总楼层数、户型、面积和朝向信息，并返回包含这些信息的列表。

    Args:
        house_info (str): 包含房屋信息的字符串。

    Returns:
        list: 包含楼层、总楼层数、户型、面积和朝向信息的列表，元素依次为字符串类型、整型、字符串类型、浮点型和字符串类型。

    """
    floor_pat = r"高楼层|中楼层|低楼层|地下室"
    total_floor_pat = r"共(\d+)层"
    house_layout_pat = r"(\d+室\d+厅)"
    house_area_pat = r"(\d+|\d+.\d+)平米"
    house_dir_pat = r"东|南|西|北"
    floor = re.findall(floor_pat, house_info)[0]
    if floor == "地下室":
        return []
    total_floor = re.findall(total_floor_pat, house_info)[0]
    house_layout = re.findall(house_layout_pat, house_info)[0]
    house_area = re.findall(house_area_pat, house_info)[0]
    house_dir = re.findall(house_dir_pat, house_info)[0]
    return [floor, int(total_floor), house_layout, float(house_area), house_dir]


def parse_follow_info(follow_info: str) -> list:
    """
    从关注信息字符串中解析出关注人数、发布时间、发布人姓名和发布人ID，并返回包含这些信息的列表。

    Args:
        follow_info (str): 包含关注信息的字符串。

    Returns:
        list: 包含关注人数、发布时间、发布人姓名和发布人ID的列表，元素依次为整型、字符串类型、字符串类型和字符串类型。
    """
    follower_num_pat = r"(\d+)人关注"
    have_upload_day_pat = r"(\d+天前发布)"
    have_upload_month_pat = r"(\d+月前发布)"
    have_upload_year_pat = r"(\d+年前发布)"
    follower_num = re.findall(follower_num_pat, follow_info)[0]
    if "天前发布" in follow_info:
        upload_date = re.findall(have_upload_day_pat, follow_info)[0]
    elif "月前发布" in follow_info:
        upload_date = re.findall(have_upload_month_pat, follow_info)[0]
    elif "年前发布" in follow_info:
        upload_date = re.findall(have_upload_year_pat, follow_info)[0]
    else:
        upload_date = ""
    return [int(follower_num), upload_date]


def parse_page(url):
    """
    解析房源页面，获取房源信息并存储至HouseInfoTable对象中

    Args:
        url (str): 待解析页面的URL

    Returns:
        None

    """
    house_info_table = HouseInfoTable()
    response = requests.get(url)
    html = lxml.etree.HTML(response.text)
    res = html.xpath('//li[@class="clear"]')
    for item in res:
        url = item.xpath('.//div[@class="title"]/a/@href')[0]
        pk = int(re.findall(r"(\d+)", url)[0])
        name = item.xpath('.//div[@class="title"]/a/@title')[0]
        location = item.xpath('.//div[@class="positionInfo"]/a/text()')[0]
        house_info_str = item.xpath('.//div[@class="houseInfo"]/text()')[1]
        house_info_list = parse_house_info(house_info_str)
        if house_info_list:
            follow_info_str = item.xpath('.//div[@class="followInfo"]/text()')[1]
            follow_info_list = parse_follow_info(follow_info_str)
            total_price = float(item.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()')[0])
            unit_price_str = item.xpath('.//div[@class="unitPrice"]/span/text()')[0]
            unit_price_pat = r"(\d+),(\d+)"
            unit_price_list = re.findall(unit_price_pat, unit_price_str)
            unit_price = int(unit_price_list[0][0] + unit_price_list[0][1])

            house_info_table.add_one_house_info(
                pk=pk,
                name=name,
                location=location,
                floor=house_info_list[0],
                total_floor=house_info_list[1],
                house_layout=house_info_list[2],
                house_area=house_info_list[3],
                house_dir=house_info_list[4],
                total_price=total_price,
                unit_price=unit_price,
                follower_num=follow_info_list[0],
                upload_time=follow_info_list[1],
            )


def worker(url_queue: queue.Queue):
    """
    从url_queue中获取URL并解析页面

    Args:
        url_queue (queue.Queue): 存储待解析URL的队列

    Returns:
        None

    """
    url = ""
    while not url_queue.empty():
        try:
            url = url_queue.get_nowait()  # 非阻塞获取URL
            logger.info(f"------> 开始解析URL：{url}")
            parse_page(url)  # 调用页面解析函数
        except queue.Empty:
            break  # 队列为空时退出循环
        except Exception as e:
            logger.error(f"解析URL {url} 时出错: {e}")
            url_queue.put(url)  # 出错时重新放入队列


def start(num_threads: int):
    """
    启动多线程爬虫程序

    Args:
        num_threads (int): 线程数量

    Returns:
        None
    """
    url_queue = get_pages_url()  # 获取URL队列
    threads = []

    # 创建并启动线程
    if url_queue:
        for _ in range(num_threads):
            t = threading.Thread(target=worker, args=(url_queue,))
            threads.append(t)
            t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    logger.info("------> 爬虫结束")
