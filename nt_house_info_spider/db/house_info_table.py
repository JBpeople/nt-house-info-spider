from datetime import datetime

from .model import HouseInfo, get_session


class HouseInfoTable(object):
    @staticmethod
    def add_one_house_info(
        pk: int,
        name: str,
        location: str,
        floor: str,
        total_floor: int,
        house_layout: str,
        house_area: float,
        house_dir: str,
        total_price: float,
        unit_price: int,
        follower_num: int,
        upload_time: str,
        score: int,
    ):
        """
        将房屋信息添加到数据库中。

        Args:
            pk (int): 房屋信息的唯一标识符。
            name (str): 房屋名称。
            location (str): 房屋所在位置。
            floor (str): 房屋所在楼层。
            total_floor (int): 房屋总楼层数。
            house_layout (str): 房屋户型。
            house_area (float): 房屋面积。
            house_dir (str): 房屋朝向。
            total_price (float): 房屋总价。
            unit_price (int): 房屋单价。
            follower_num (int): 房屋关注人数。
            upload_time (str): 房屋信息上传时间。
            score (int): 房源评分。

        Returns:
            None
        """
        house_info = HouseInfo(
            pk=pk,
            name=name,
            location=location,
            floor=floor,
            total_floor=total_floor,
            house_layout=house_layout,
            house_area=house_area,
            house_dir=house_dir,
            total_price=total_price,
            unit_price=unit_price,
            follower_num=follower_num,
            upload_time=upload_time,
            score=score,
        )
        with get_session() as session:  # type: ignore [attr-defined]
            session.add(house_info)
            session.commit()

    @staticmethod
    def query(
        pk: int = 0,
        name: str = "",
        location: str = "",
        floor: str = "",
        total_floor: int = 0,
        house_layout: str = "",
        house_area: float = 0,
        house_dir: str = "",
        follower_num: int = 0,
        upload_time: datetime = datetime.min,
    ) -> list[HouseInfo]:
        """
        查询房屋信息。

        Args:
            pk (int): 房屋信息的唯一标识符。
            name (str): 房屋名称。
            location (str): 房屋所在位置。
            floor (str): 房屋所在楼层。
            total_floor (int): 房屋总楼层数。
            house_layout (str): 房屋户型。
            house_area (float): 房屋面积。
            house_dir (str): 房屋朝向。
            follower_num (int): 房屋关注人数。
            upload_time (datetime): 房屋信息上传时间。
        Returns:
            list[HouseInfo]
        """

        q = []
        if pk:
            q.append(HouseInfo.pk == pk)
        if name:
            q.append(HouseInfo.name == name)
        if location:
            q.append(HouseInfo.location == location)
        if floor:
            q.append(HouseInfo.floor == floor)
        if total_floor:
            q.append(HouseInfo.total_floor == total_floor)
        if house_layout:
            q.append(HouseInfo.house_layout == house_layout)
        if house_area:
            q.append(HouseInfo.house_area == house_area)
        if house_dir:
            q.append(HouseInfo.house_dir == house_dir)
        if follower_num:
            q.append(HouseInfo.follower_num == follower_num)
        if upload_time:
            q.append(HouseInfo.upload_time == upload_time)
        with get_session() as session:  # type: ignore [attr-defined]
            return session.query(HouseInfo).filter(*q).all()
