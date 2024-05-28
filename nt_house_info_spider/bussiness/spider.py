import re
from queue import Queue

import lxml
import lxml.etree
import requests

from nt_house_info_spider.db.house_info_table import HouseInfoTable
from nt_house_info_spider.log import logger
from nt_house_info_spider.static import constant

URL_QUEUE: Queue = Queue()


def get_pages_url():
    """
    获取房源列表页的所有页面URL并放入队列中

    Args:
        无参数

    Returns:
        无返回值，将获取到的页面URL放入URL_QUEUE队列中

    """
    response = requests.get(constant.URL)
    html = lxml.etree.HTML(response.text)
    res = html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')
    try:
        page_info = eval(res[0])
        page_num = page_info["totalPage"]
        logger.info(f"------> 获取总页数成功{page_num}")
    except IndexError:
        logger.error("-----> 获取总页数失败")
        return
    for i in range(1, page_num + 1):
        url = constant.URL + f"pg{i}/"
        URL_QUEUE.put(url)


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
            total_price = float(
                item.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()')[0]
            )
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


def start():
    """
    执行爬虫主程序

    Args:
        无参数

    Returns:
        无返回值

    """

    get_pages_url()
    while URL_QUEUE.empty() is False:
        url = URL_QUEUE.get()
        logger.info(f"------> 开始解析URL：{url}")
        parse_page(url)
    logger.info("------> 爬虫结束")
