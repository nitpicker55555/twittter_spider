# -*- coding: utf-8 -*-
# Splitting the text using the specified delimiter
import queue,re
import random
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from functools import wraps
import json, os
from selenium.common.exceptions import NoSuchElementException
# from infoweb_client import send_message_to_server
import asyncio,mmap
# from selenium.webdriver.chrome.service import Service
"""
cd C:\Program Files\Google\Chrome\Application
chrome.exe --remote-debugging-port=9222 --disable-web-security --user-data-dir=remote-profile  


start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --disable-web-security --user-data-dir=remote-profile
timeout /t 1
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --disable-web-security --user-data-dir=remote-profile2
timeout /t 1
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --disable-web-security --user-data-dir=remote-profile3
timeout /t 1
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9225 --disable-web-security --user-data-dir=remote-profile4

"""

"""
ai ethics  until:2021-01-01 since:2015-01-01 -filter:links -filter:replies
ai ethics min_faves:1 until:2021-01-01 since:2020-01-01 -filter:links -filter:replies
"""

"""
profile getzpz@qq.com
gtzpz@foxmail.com
2 ge42key@tum.de
3 a1303385763@163.com ppcc2
4 15114829291@qq.com
ge42key@mytum.de
"""

# dict_list = []
profile_dict = {}


def handle_stale_reference(retries=2, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("exception in decoration",e)
                    try:
                        print(args,"handle_stale_reference args")
                        driver = args[1]  # 假设第一个参数是 WebDriver 实例
                        driver.find_element_by_xpath("//*[contains(text(), 'This account doesn’t exist')]")
                        print("找到字符串 'This account doesn’t exist'，中断执行。")
                        break
                        # raise Exception("AccountNotExistException")  # 抛出一个自定义异常或进行其他中断操作
                    except NoSuchElementException:
                        # 如果没有找到该字符串，则等待后重试
                        time.sleep(delay)
                    # time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@handle_stale_reference()
def selenium_spider(elements,driver,date_str):
    dict_list = []
    # xpath_str='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[2]/span/span'
    # """
    # /html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[9]/div/div/article/div/div/div[2]/div[2]/div[2]/div
    # """
    #
    # xpath_str='/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[2]/div'
    # elements = driver.find_elements_by_xpath(xpath_str)

    for element in elements:
        user_each = {}
        link = element.find_element_by_xpath('../../div[1]/div/div[1]/div/div/div[2]/div/div[1]/a').get_attribute(
            'href')
        # speaker=element.find_element_by_xpath('../../div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span').text
        user_name = element.find_element_by_xpath('../../div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
        try:
            time_str = element.find_element_by_xpath(
                '../../div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time').get_attribute('datetime')

            print(user_name, time_str)
        except:
            time_str=date_str
        # print(link)
        # liked_str=element.find_element_by_xpath('../../div[3]/div/div[3]/div/div/div[2]/span/span/span').text
        try:
            element_items = element.find_element_by_xpath('../..')
            element_item = element_items.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
            liked_num = element_item.find_element_by_xpath('.//div/div[2]/span/span/span').text
            print(liked_num)
        except:  #
            liked_num = "0"
        try:
            element_items = element.find_element_by_xpath('../..')
            element_item = element_items.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
            retweets_num = element_item.find_element_by_xpath('.//div/div[2]/span/span/span').text
            print(retweets_num)
        except:  #
            retweets_num = "0"
        try:
            element_items = element.find_element_by_xpath('../..')
            element_item = element_items.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
            reviews_num = element_item.find_element_by_xpath('.//div/div[2]/span/span/span').text
            print(reviews_num)
        except:  #
            reviews_num = "0"

        speaker_content = element.text

        # print(speaker_content)
        print('"________________________"')
        user_each['time'] = time_str
        user_each['user_name'] = user_name
        user_each['link'] = link
        user_each['content'] = speaker_content
        user_each['liked_num'] = liked_num
        user_each['retweets_num'] = retweets_num
        user_each['reviews_num'] = reviews_num
        dict_list.append(user_each)

    return dict_list


def simulated_scroll(driver, min_pixels=300, max_pixels=800, steps=5):
    steps = random.randint(3, 9)
    delay = random.uniform(1, 3)
    time.sleep(delay)
    direction = 1  # -1 表示向上滚动，1 表示向下滚动
    total_scroll_amount = direction * random.randint(min_pixels, max_pixels)
    scroll_per_step = total_scroll_amount / steps

    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_per_step});")
        time.sleep(random.uniform(0.05, 0.2))  # 在每一步之间短暂地随机暂停
    delay = random.uniform(1, 2)
    time.sleep(delay)
    direction = -1  # -1 表示向上滚动，1 表示向下滚动
    total_scroll_amount = direction * random.randint(min_pixels, max_pixels)
    scroll_per_step = total_scroll_amount / steps

    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_per_step});")
        time.sleep(random.uniform(0.05, 0.2))  # 在每一步之间短暂地随机暂停


@handle_stale_reference()
def get_geo(url, driver):
    print("get_geo", url)
    if url != "0":
        delay = random.uniform(5, 15)
        # time.sleep(delay)
        print("get_geo", delay)
        driver.get(url)

    else:
        pass
        # all_handles = driver.window_handles
        # driver.switch_to.window(all_handles[0])



    icon_verified=None
    joined_time=None
    UserUrl=None
    UserDescription=None
    UserProfessionalCategory=None
    UserLocation=None
    following = None
    follower = None
    Subscription = None
    posts_num = "0"
    try:
        # 尝试查找“Yes, view profile”按钮
        button = driver.find_element_by_xpath("//*[contains(text(), 'Yes, view profile')]")

        # 如果找到了，就点击它
        button.click()
        print("Yes, view profile Click")
    except:
        pass
    try:
        follower_str = '//*[@class="css-175oi2r r-ymttw5 r-ttdzmv r-1ifxtd0"]/span'

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, follower_str))
        )
    except:
        pass
    simulated_scroll(driver)
    try:
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserLocation"]')
        UserLocation = element.find_element_by_xpath('.//span/span').text
        print(UserLocation)
    except:  #
        UserLocation = None
    try:
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserProfessionalCategory"]')
        UserProfessionalCategory = element.find_element_by_xpath('.//span/span').text
        print(UserProfessionalCategory)
    except:  # UserProfessionalCategory
        UserProfessionalCategory = None
    try:
        driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div//*[@aria-label="Verified account"]')
        print("'Verified account' found.")
        icon_verified = True


    except:  # UserProfessionalCategory,NoSuchElementException
        print("not Verified.")
        icon_verified = False
    try:
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserJoinDate"]')
        joined_time = element.find_element_by_xpath('.//span').text
        print(joined_time)
    except:
        joined_time = None
    try:
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserUrl"]')
        UserUrl = element.find_element_by_xpath('.//span').text
        print(UserUrl)
    except:
        UserUrl = None
    try:
        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserDescription"]')
        UserDescription = element.text
        print(UserDescription)
    except:
        UserDescription = None
    follower_str = '//*[@class="css-175oi2r r-13awgt0 r-18u37iz r-1w6e6rj"]'
    try:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, follower_str))
            )
        finally:
            print("follower_str pass---")
            follower_following = driver.find_elements_by_xpath(follower_str)
            for item_ in follower_following:
                print("follower_str ", item_.text)

                if "Following" in item_.text:
                    # following = item_.find_element_by_xpath('../../span').text
                    following = re.search(r'(\d[\d,]*) Following', item_.text).group(1)
                    print("following: ", following)
                if "Followers" in item_.text:
                    follower = re.search(r'(\d[\d,]*) Followers', item_.text).group(1)
                    print("follower: ", follower)
                if "Subscription" in item_.text:

                    # Subscription = item_.find_element_by_xpath('../../span').text
                    Subscription = re.search(r'(\d[\d,]*) Subscription', item_.text).group(1)
                    print("Subscription: ", Subscription)


                follower_str = '//*[@class="css-901oao css-1hf3ou5 r-1bwzh9t r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0"]'
                follower_following = driver.find_elements_by_xpath(follower_str)
                for item_ in follower_following:
                    if "posts" in item_.text:
                        posts_num = item_.text

                    # posts_num_xpath="//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div"
                try:
                    elements_containing_posts = driver.find_elements_by_xpath("//*[contains(text(), 'posts')]")[0]
                    posts_num = elements_containing_posts.text
                    print("posts_num_xpath", posts_num)
                except Exception as e:
                    print("posts getting error ", e)
                print("posts_num", posts_num)
    except:
        print("-----")
        pass


    result_dict = {'UserProfessionalCategory': UserProfessionalCategory, 'UserLocation': UserLocation,
                   'follower': follower, 'following': following, 'Subscription': Subscription,
                   'verified': icon_verified, 'joined_time': joined_time, 'UserUrl': UserUrl,
                   'UserDescription': UserDescription, 'posts_num': posts_num}

    return result_dict


# selenium_spider()
@handle_stale_reference()
def iteration(url, driver,num,date_str):
    xpath_str = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[2]/div'
    old_count = 0
    elements_pre = []
    # all_handles = driver.window_handles
    # driver.switch_to.window(all_handles[-1])

    driver.get(url)
    delay = random.uniform(2, 27)
    time.sleep(delay)
    dict_list = []
    while True:
        # 使用JavaScript来滚动页面
        # 使用您的XPath获取元素

        stuck_num = 0
        elements = driver.find_elements_by_xpath(xpath_str)
        while len(elements)==0:
            elements = driver.find_elements_by_xpath(xpath_str)
            print("Thread", num, len(elements))
            if len(elements) == 0:
                print("Thread",num,"no tweet found")
                try:
                    xpath_no_results = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/span'

                    element = driver.find_element_by_xpath(xpath_no_results).text
                    print("异常: ", element)
                    if element != "Retry":
                        print("没有结果")
                        break
                    else:
                        print("卡住了")


                except:
                    print("Thread", num, "no tweet found but no Retry")
                    elements = driver.find_elements_by_xpath(xpath_str)
                    print("Thread", num, len(elements))
                    break
                stuck_num += 1
                print("卡住了", stuck_num)
                delay = random.uniform(50, 60) * stuck_num
                # asyncio.run(send_message_to_server(["Stuck Thread:", str(num), "Retry after %s seconds"%str(delay)[0:4]]))
                time.sleep(300 + delay)
                driver.refresh()
            else:
                stuck_num = 0
                break
        elements_new = [item for item in elements if item not in elements_pre]
        dict_list.extend(selenium_spider(elements_new,driver,date_str))
        elements_pre = elements_pre + elements_new

        print(len(elements_pre), "elements:", len(elements), "elements_new", len(elements_new))
        # 检查新元素数量是否增加
        if len(elements_pre) <= old_count:
            break  # 如果元素数量没有增加，跳出循环
        old_count = len(elements_pre)
        scroll_func(driver)
        # 为页面加载新的推文等待几秒
        delay = random.uniform(1, 8)
        time.sleep(delay)
    return dict_list
def count_lines(filename):
    with open(filename, "r+") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        return mmapped_file.read().count(b'\n')

def iteration_profile(data_queue, lock, num,with_profile_file,keyword_replace):
    # all_handles = driver.window_handles
    # driver.switch_to.window(all_handles[0])
    options = Options()
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])

    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(num))
    options.add_argument('--disable-blink-features=AutomationControlled')
    # service = Service(r"C:\Users\Mengyu\Downloads\twitter_spider\twitter_spider\chromedriver.exe")
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options,
                              executable_path=r"C:\Users\Morning\Desktop\hiwi\gpt_score\twitter_spider\twitter_spider\chromedriver.exe")
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    while True:
        try:
            item_ = data_queue.get(timeout=3)
        except:
            break

        if item_['link'] not in profile_dict:

            profile_dict[item_['link']] = get_geo(item_['link'], driver)
        else:
            print("link alreday in.....")
        item_.update(profile_dict[item_['link']])
        try:
            sum_lines=count_lines(with_profile_file)
        except:
            sum_lines=0
        # without_profile_file_sum_lines = count_lines(str(with_profile_file).replace("with","without"))
        # process_percentage=(sum_lines/without_profile_file_sum_lines)*100
        # asyncio.run (send_message_to_server(["Processed_file",with_profile_file, "Processed_percentage: {:.2f}%".format(process_percentage),"Processed_lines:",sum_lines]))

        with lock:
            with open(with_profile_file, "a") as file:
                file.write(json.dumps(item_) + "\n")
        data_queue.task_done()



def url_time_test(data_queue, lock, num, without_profile_file,keyword_replace):
    print(num, "work!")

    def create_twitter_search_url(query):
        # 使用 urllib.parse.quote_plus 来确保字符串被正确编码为 URL 格式
        from urllib.parse import quote_plus

        base_url = "https://twitter.com/search?f=top&q="
        encoded_query = quote_plus(query)  # 对输入字符串进行URL编码
        url = f"{base_url}{encoded_query}{{}}{{}}&src=typed_query"

        return url
    while True:
        try:
            since_date = data_queue.get(timeout=3)
        except queue.Empty:
            break
        options = Options()
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])

        options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(num))
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # service=Service(r"C:\Users\Mengyu\Downloads\twitter_spider\twitter_spider\chromedriver.exe")
        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\Morning\Desktop\hiwi\gpt_score\twitter_spider\twitter_spider\chromedriver.exe")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # keyword_replace=keyword_replace.replace(" ","%20")
        base_url = create_twitter_search_url(keyword_replace)
        # base_url = "https://twitter.com/search?f=top&q=thanks%20chatgpt%20and%20ai%20{}%20{}&src=typed_query"

        until_date = (since_date + timedelta(days=1)).strftime('%Y-%m-%d')
        url_need = base_url.format(" since:" + str(since_date.strftime('%Y-%m-%d')), " until:" + str(until_date))
        print(url_need)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        dict_list = iteration(url_need, driver,num,str(since_date.strftime('%Y-%m-%d')))
        try:
            sum_lines=count_lines(without_profile_file)
        except:
            sum_lines=0
        # process_percentage=year_percentage(until_date)
        # asyncio.run (send_message_to_server(["Processed_file",without_profile_file, "Processed_percentage: {:.2f}%".format(process_percentage),"Processed_lines:",sum_lines,"Page_right_now:",str(since_date.strftime('%Y-%m-%d')),"this_page:",len(dict_list)]))
        print("start to write in file")
        with lock:
            for i in dict_list:
                with open(without_profile_file, "a") as file:
                    file.write(json.dumps(i) + "\n")
        data_queue.task_done()


def scroll_func(driver):
    # 1. 查找元素列表
    def gradual_scroll(driver, target_element, steps=10, chance_to_scroll_up=0.2):
        target_location = target_element.location['y']
        current_location = driver.execute_script('return window.pageYOffset;')
        step_size = (target_location - current_location) / steps

        for _ in range(steps):
            if random.random() < chance_to_scroll_up:
                # 随机向上滚动一些
                scroll_up_distance = random.uniform(10, 20)  # 随机决定向上滚动的距离，你可以根据需要调整这些值
                print(driver, "向上滚动", scroll_up_distance)
                current_location -= scroll_up_distance
                driver.execute_script(f'window.scrollTo(0, {current_location});')
                time.sleep(random.uniform(0.1, 0.3))

            # 常规的向下滚动
            current_location += step_size
            driver.execute_script(f'window.scrollTo(0, {current_location});')
            time.sleep(random.uniform(0.1, 0.4))
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
        except Exception as e:  # Catch the exception when element is not found
            print("滚动报错")
            # If target_element is not found, scroll down by a page length
            viewport_height = driver.execute_script("return window.innerHeight;")
            driver.execute_script(f'window.scrollTo(0, {current_location + viewport_height});')

    # 使用代码
    xpath_str = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/div/div/article/div/div/div[2]/div[2]/div[2]/div'

    elements = driver.find_elements_by_xpath(xpath_str)
    last_element = elements[-1]
    gradual_scroll(driver, last_element)


def missing_dates(file_path):
    dates = []
    with open(file_path, "r") as file:
        for line in file:
            data = json.loads(line)
            date_str = data["time"].split("T")[0]
            dates.append(date_str)

    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    min_date = min(dates)
    max_date = max(dates)

    all_dates = set(min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1))

    missing_dates = all_dates - set(dates)
    return missing_dates


def last_date_in_file(file_path):
    times = []
    with open(file_path, "r") as file:
        for line in file:
            data = json.loads(line)
            if "time" in data:
                times.append(data["time"])

    # Find the latest time
    latest_time = max(times) if times else None
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_object = datetime.strptime(latest_time, date_format)

    # Add one day to the date
    new_date_object = date_object + timedelta(days=1)
    new_date = new_date_object.strftime("%Y-%m-%d")

    start_date = datetime.strptime(new_date, "%Y-%m-%d")

    print(new_date)

    return start_date


# data_transfer()

def year_percentage(date_str):
    try:
        print(date_str,"===")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_of_year = datetime(date.year, 1, 1)

        # Check if it's a leap year
        if date.year % 4 == 0 and (date.year % 100 != 0 or date.year % 400 == 0):
            total_days = 366
        else:
            total_days = 365

        days_passed = (date - start_of_year).days + 1  # Add 1 because we count the start day itself

        percentage = (days_passed / total_days) * 100
    except Exception as e:
        print(e,"error")
        percentage="0"
    return percentage


def multitask(mode, startdate_set="", enddate_set="",keyword_replace=""):
    time_start = time.time()
    without_profile_file = keyword_replace+startdate_set + "_" + enddate_set + "_" + "without_profile.jsonl"
    # with_profile_file = keyword_replace+startdate_set + "_" + enddate_set + "_" + "with_profile.jsonl"
    with_profile_file =  "key_word_list_with_profile.jsonl"

    threads = []
    missing_list = []
    lock = threading.Lock()
    data_queue = queue.Queue()
    if mode == "content":
        target_func = url_time_test
        try:
            start_date = last_date_in_file(without_profile_file)
            missing_list = missing_dates(without_profile_file)
        except:
            start_date = datetime.strptime(startdate_set, "%Y-%m-%d")
        end_date = datetime.strptime(enddate_set, "%Y-%m-%d")
        print("Spider process From", start_date, "to", end_date)

        delta = timedelta(days=1)
        current_date = start_date

        while current_date <= end_date:
            data_queue.put(current_date)
            current_date += delta
        if missing_list != []:
            for i in missing_list:
                data_queue.put(i)
            print("Adding missing dates", missing_list)
        _file = without_profile_file
    elif mode=="profile":

        target_func = iteration_profile
        processed_list = []
        file_path = with_profile_file
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    data = json.loads(line.strip())
                    processed_list.append(data['content'])  # 避免重复读取

                    keys = list(data.keys())
                    index_reviews_num = keys.index("reviews_num")
                    link_value = data["link"]
                    sub_dict = {key: data[key] for key in keys[index_reviews_num + 1:]}
                    profile_dict[link_value] = sub_dict
        except:
            pass
        file_path = without_profile_file
        print("processed list: ", len(processed_list))
        with open(file_path, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                if data['content'] not in processed_list:
                    data_queue.put(data)
                else:
                    pass
                    # print("processed item..")
        _file=with_profile_file
    for i in range(6):
        delay = random.uniform(1, 4)
        print(i, "delay", delay)
        # time.sleep(delay)

        t = threading.Thread(target=target_func, args=(data_queue, lock, i + 9222, _file,keyword_replace))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    time_end = time.time()
    time_sum = (time_end - time_start) / 3600
    print("用时: %s hour"%time_sum)
    # os.system("shutdown /s /t 1")
ai_ethics_topics = [
    "Artificial Intelligence ethics",
    "Ethics of AI",
    "Ethics In AI",
    "AI for good",
    "Ethical AI"
]
# multitask("content", "2023-1-1", "2023-12-31")
# multitask("profile", "2022-1-1", "2022-12-31")
# multitask("content", "2021-1-1", "2021-12-31")
for i in ai_ethics_topics:
    for time_ in range(15,23):

        multitask("content", "20%s-1-1"%time_, "20%s-12-31"%time_,i)
# multitask("content", "2020-1-1", "2020-12-31")
# multitask("profile", "2020-1-1", "2020-12-31")
# multitask("content", "2019-1-1", "2019-12-31")
# multitask("profile", "2019-1-1", "2019-12-31")
# multitask("content", "2018-1-1", "2018-12-31")
# multitask("profile", "2018-1-1", "2018-12-31")
#
# multitask("content", "2017-1-1", "2017-12-31")
# multitask("profile", "2017-1-1", "2017-12-31")
#
# multitask("content", "2016-1-1", "2016-12-31")
# multitask("profile", "2016-1-1", "2016-12-31")
#
# multitask("content", "2015-1-1", "2015-12-31")
# multitask("profile", "2015-1-1", "2015-12-31")
