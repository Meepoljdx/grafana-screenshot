import sys
from selenium import webdriver
import time
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

if __name__ == "__main__":

    url = sys.argv[1]
    output = sys.argv[2]
    options = Options()
    # options.headless = True
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument("--headless")

    options.binary_location = ("/opt/firefox/firefox")
    # 设置代理配置
    # options.set_preference("network.proxy.type", 1)
    # options.set_preference("network.proxy.http", "127.0.0.1")
    # options.set_preference("network.proxy.http_port", 8443)
    driver = webdriver.Firefox(options=options, service=Service(executable_path="./driver/geckodriver"))
    driver.set_window_size(1920, 1080)
    driver.get(url)
    time.sleep(5)
    # grafana的懒加载，需要模拟完整下滑
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 获取浏览器窗口的高度
    window_height = driver.execute_script("return window.innerHeight;")
    # 获取页面的总高度
    page_height = driver.execute_script("return document.body.scrollHeight;")
    # 当前滚动位置
    scroll_position = 0
    while scroll_position < page_height:
        # 滚动一屏
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        # 更新滚动位置
        scroll_position += window_height
        # 等待一段时间，以便页面有时间加载（如果有无限滚动的内容）
        time.sleep(1)

    driver.get_full_page_screenshot_as_file(output)
    driver.quit()
