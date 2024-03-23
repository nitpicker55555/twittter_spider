from selenium_basic_func import *
# https://twitter.com/petervan
# print("get_geo", url)




icon_verified = None
joined_time = None
UserUrl = None
UserDescription = None
UserProfessionalCategory = None
UserLocation = None
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
# simulated_scroll(driver)
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
        print(follower_following, 'follower_following')
        for item_ in follower_following:
            print("follower_str", item_.text)

            if "Following" in item_.text:
                # following = item_.find_element_by_xpath('../../span').text
                following = re.search(r'([\d,.K]+) Following', item_.text).group(1)
                print("following: ", following)
            if "Followers" in item_.text:
                follower = re.search(r'([\d,.K]+) Followers', item_.text).group(1)
                print("follower: ", follower)
            if "Subscription" in item_.text:
                # Subscription = item_.find_element_by_xpath('../../span').text
                Subscription = re.search(r'([\d,.K]+) Subscription', item_.text).group(1)
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
except Exception as e:
    print("-----",e)
    # pass

result_dict = {'UserProfessionalCategory': UserProfessionalCategory, 'UserLocation': UserLocation,
               'follower': follower, 'following': following, 'Subscription': Subscription,
               'verified': icon_verified, 'joined_time': joined_time, 'UserUrl': UserUrl,
               'UserDescription': UserDescription, 'posts_num': posts_num}

print(result_dict)
