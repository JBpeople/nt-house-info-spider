import os
import sys

from loguru import logger

path = os.path.join("log")

logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
handler_id = logger.add(sys.stderr, level="INFO")  # 添加一个可以修改控制的handler，只有INFO以上的日志才会在终端输出

# 设置INFO等级以上的日志输出，展示给用户看的
logger.add(
    os.path.join(path, "{time:YYYY-MM-DD}.log"),
    filter=lambda msg: "DEBUG" not in msg,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    retention="10 days",
    rotation="00:00",
    level="INFO",
)

# 设置DEBUG等级以上的日志输出，展示给开发人员看的
logger.add(
    os.path.join(path, "{time:YYYY-MM-DD}-DEBUG.log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    retention="10 days",
    rotation="00:00",
    level="DEBUG",
)
