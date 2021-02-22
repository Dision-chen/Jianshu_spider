import time
import random
from selenium import webdriver
from scrapy.http import HtmlResponse


class JianshuDownloaderMiddleware:
    def __init__(self):
        opt = webdriver.ChromeOptions()
        # opt.add_argument('--headless')  # 浏览器不提供可视画面
        opt.add_argument('--user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/88.0.4324.104 Safari/537.36')  # 设置请求头
        opt.add_argument('https://book.jd.com/booksort.html')
        self.driver = webdriver.Chrome(options=opt)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        all_window_height = []  # 创建一个列表，用于记录每一次拖动滚动条后面的最大高度
        all_window_height.append(self.driver.execute_script("return document.body.scrollHeight;"))  # 当前页面的最大高度加入列表
        while True:
            self.driver.execute_script("scroll(0,100000)")  # 执行拖动滚动条操作
            time.sleep(3)
            check_height = self.driver.execute_script("return document.body.scrollHeight;")
            if check_height == all_window_height[-1]:  # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
                break
            else:
                all_window_height.append(check_height)  # 如果不想等，将当前页面最大高度加入列表。
        html = self.driver.page_source  # 获取页面源码
        return HtmlResponse(url=request.url, body=html.encode())

    def close(self, spider):
        self.driver.quit()
