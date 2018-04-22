#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================
# 模拟 chrome 浏览器登录脚本
# ========================


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageEnhance
import time
import random

def get_average(img):
  total = 0
  pixels = 0
  for y in range(0, img.size[1]):
    for x in range(round(img.size[0] / 2), img.size[0]):
      pixels += img.getpixel((x, y))
      total += 1

  return (pixels / total)


def get_position(img, loca, ave):
  start = int(img.size[0] / 2)
  width = 51
  thre = 0
  freq = int(((img.size[0] / 2) - width) / 5)

  maxvar = {"x": 0, "y": loca, "var": 0}

  if ave > 150:
    thre = 110
  else:
    thre = 55

  for offset in range(0, freq):
    total = 0
    pixels = 0
    start_x = offset * 5 + start

    for y in range(maxvar["y"], maxvar["y"] + width):
      for x in range(offset * 5 + start, offset * 5 + start + width):
        if img.getpixel((x, y)) < thre:
          total += 1

    if total > maxvar["var"]:
      maxvar["x"] = offset * 5 + start
      maxvar["var"] = total

  return maxvar

def pri_cookie(cookies):
  for cookie in cookies:
    print("%s : %s" % (cookie["name"], cookie["value"]))
  
def operating(driver, fankd):
  huak = driver.find_element_by_xpath("//*[@id='tcaptcha_drag_button']")

  ActionChains(driver).click_and_hold(on_element=huak).perform()
  time.sleep(2)

  ydong = fankd["x"] - 39
  while(ydong > 1):
    ActionChains(driver).move_by_offset(2, 0).perform()
    ydong -= 2
    time.sleep(0.002 * random.randint(1, 10))

  time.sleep(1)

  ActionChains(driver).release(on_element=huak).perform()


def verification(driver):
  try:
    driver.find_element_by_xpath("//*[@id='tcaptcha_iframe']")
  except Exception as e:
    return 0
  return 1


if __name__ == "__main__":
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 5.0; SM-G9550 "
                       "Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 "
                       "Mobile Safari/537.36")

  # chromedriver path
  driver = webdriver.Chrome(
      executable_path="chromedriver",
      chrome_options=options)
  driver.set_window_size(400, 700)

  try:
    driver.get("https://passport.qidian.com/")
    time.sleep(5)
  except Exception as e:
    print("***** 获取网页失败! *****")
    print(e)
    driver.close()
    driver.quit()

  # 要修改成自己的帐号密码
  input_un = driver.find_element_by_xpath("//*[@id='username']")
  input_un.send_keys("username")
  input_pw = driver.find_element_by_xpath("//*[@id='password']")
  input_pw.send_keys("password")

  login_btn = driver.find_element_by_xpath(
      "//*[@class='login-wrap input-list']/a")
  login_btn.click()
  time.sleep(10)

  flag = 1
  limit = 0
  while(True):
    if driver.current_url == "https://m.qidian.com/":
      print("***** 成功登录! *****")
      pri_cookie(driver.get_cookies())
      limit = 0
      break
    else:
      if(limit >= 10):
        print("***** 超出尝试上限! *****")
        break
      else:
        limit += 1
        print("***** 第" + str(limit) + "次尝试 *****")

      if limit == 1:
        try:
          iframe = driver.find_element_by_xpath("//*[@id='tcaptcha_iframe']")
          ifloc = iframe.location
          driver.switch_to.frame(iframe)
        except Exception as e:
          print("***** 密码错误! *****")
          break
      elif limit > 1 and verification(driver):
        print("***** 密码错误! *****")
        break
      elif limit > 1:
        print("***** 验证失败... *****")
        print("***** 重新验证... *****")
      else:
        print("***** 未知错误! *****")
        break

      yanzgma = driver.find_element_by_xpath("//img[@id='bkBlock']")
      yaloc = yanzgma.location
      yasiz = yanzgma.size

      driver.get_screenshot_as_file("q1.png")
      rangle = (int(ifloc['x'] + yaloc['x']), int(ifloc['y'] + yaloc['y']),
                int(ifloc['x'] + yaloc['x']) + yasiz['width'],
                int(ifloc['y'] + yaloc['y']) + yasiz['height'])

      img = Image.open("q1.png")
      img = img.convert("L")
      img = img.crop(rangle)
      fank = driver.find_element_by_xpath("//*[@id='slideBlock']").location
      kloc = fank["y"] - yanzgma.location["y"] + 8
      fankd = get_position(img, kloc, get_average(img))
      img.close()

      print("***** 移动滑块... *****")
      operating(driver, fankd)
      time.sleep(10)

  driver.close()
  driver.quit()
