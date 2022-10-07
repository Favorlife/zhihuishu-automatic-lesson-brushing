import sys

import selenium
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains



from CrackSlider import CrackSlider


url = 'https://passport.zhihuishu.com/login'

#web = Chrome()
#web.get('https://www.zhihuishu.com/')



#*****************************************************************************************

def find_class(driver,num):
    driver.find_element(By.XPATH, '//*[@id="headerMain"]/ul/li[4]/a').click()
    time.sleep(3)

    #关闭‘切换身份提醒’,一般要点两次
    try:
        # driver.find_element(By.XPATH,'//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]').click()
        # driver.find_element(By.XPATH, '//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]').click()
        #上面两个是测试账号课堂的路径，非学生绑定账号


        driver.find_element(By.XPATH,'//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]').click()
        driver.find_element(By.XPATH, '//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]').click()  #这两个是学生账号登录后的路径
    except Exception as e:
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]').click()
        driver.find_element(By.XPATH, '//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]').click()

    #定位到课程，这个num是想要由上往下课程的序号
    Xp = f'//*[@id="sharingClassed"]/div[2]/ul[{num}]/div/dl/dt/div[1]/div[1]'
    driver.find_element(By.XPATH,Xp).click()


    time.sleep(4)
    #关闭诚信学习警告-我知道了  和 学前必读
    try:
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[6]/div/div[3]/span/button').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="app"]/div/div[7]/div[2]/div[1]/i').click()
    except Exception as e:
        print('start class error')
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[6]/div/div[3]/span/button').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[1]/i').click()



#自动播放视频*******************************************************************************
def play():
    while True:
        try:
            #定位到播放按钮
            time.sleep(2)
            play_button = driver.find_element(By.XPATH, '//*[@id="playButton"]')
            next_button = driver.find_element(By.XPATH, '//*[@id="nextBtn"]')

            play_button.click()

            #写入更改倍速的js
            speed_script = '''
            function changeSpeed(){
            var x = document.querySelector('.speedTab10');
            x.setAttribute('rate','16.0');
            }
            changeSpeed()
            '''
            driver.execute_script(speed_script)

            #点击更改倍速为 1.25， 实现x16倍速
            time.sleep(0.5)
            speed_button = driver.find_element(By.XPATH,'//*[@id="vjs_container"]/div[10]/div[8]/span')
            ActionChains(driver).move_to_element(speed_button).perform()
            speed_125 = driver.find_element(By.XPATH,'//*[@id="vjs_container"]/div[10]/div[8]/div/div[2]')
            speed_125.click()
            return
        except Exception as e:
            driver.refresh()
            print('play error, refresh successful')




def play_not_finished(all_units):
    index = find_not_finished(Class_list)
    if index == None:
        print("You've finished watching your online course.")
        return True
    while index!=None:
        index = find_not_finished(Class_list)
        print(f'准备播放{index}')

        #跳转到未完成的课程
        while True:

            if all_units[0].text == index:   #如果按顺序找到了没有播放的课程小节号，则点击跳转
                try:
                    all_units[0].click()   #点击跳转
                    break
                except:
                    driver.refresh()
            else:
                print('locating')
                all_units.pop(0)  #如果不等，则说明已经看过了，pop掉

        #time.sleep()
        #播放
        play()

        #检测是否播放完成(另起一个线程，在播放过程中循环检测，直到检测为finished则结束)
        global res
        res = False  #存放返回值
        #
        # thread_judge = Thread(target=judge)
        # thread_judge.start()   #开始循环检测


        while True:
            judge()
            temp_res = res
            if res != True:
                print(f'continue{index}:{res}', end='-->-->')
                time.sleep(6)
                judge()
                if (temp_res == res) and res!=True:   #5秒后进度不变 可能是结束了也可能是暂停了
                    print('进度条没变化，再次点击播放键')
                    #重新播放
                    while True:
                        try:
                            time.sleep(1)
                            play_button = driver.find_element(By.XPATH, '//*[@id="playButton"]')
                            play_window = driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
                            ActionChains(driver).move_to_element(play_window).perform()
                            time.sleep(1)
                            play_button.click()
                            break
                        except:
                            driver.refresh()



            elif res == True:
                print(f'end{index}')
                Class_list.pop(0)
                all_units.pop(0)
                break
    print("You've finished watching your online course.")
    return True


#获取当前课程的所有课的列表
def Class_list_init():
    #通过js返回
    #课程列表
    script1 = r'''
    function getInfo() {
        var infoList = [];
        var lessons = [];
        var toBeContinued = [];
        var video = document.querySelectorAll('.video');
        for (var i = 0; i < video.length; i++) {
            var lesson = {};
            var titleAll = video[i].innerText;
            var titlereg = /(.*)\n(.*)\n(.*)/;
            var info = titlereg.exec(titleAll);
            lesson['unit'] = info[1];
            lesson['title'] = info[2];
            lesson['time'] = info[3];
            var all = video[i].innerHTML;
            var reg = /(.*)time_icofinish(.*)/;
            reg.compile(reg);
            lesson['finish'] = reg.test(all);
            lessons[i] = lesson;
            if (!lesson['finish']) {
                toBeContinued.push(i);
            }
        }
        infoList.push(lessons);
        infoList.push(toBeContinued);
        return infoList;
    }
    return getInfo()
    '''

    all_list = driver.execute_script(script1)    #return 2 array
    # all_list[0]:  example: 'finish': True/faulse, 'time': '00:07:11', 'title': '引言', 'unit':0.1
    # all_list[1]:  not finished class



    return all_list

#判断是否看完当前课程
def is_finished():
    script = '''
        function currentFinish() {
        var current = document.querySelectorAll('.current_play')[0].outerHTML;
        var reg = /(.*)time_icofinish(.*)/;
        reg.compile(reg);
        if(reg.test(current)){
        return true;
        }else{
        return document.querySelector('.current_play .progress-num').innerHTML;
        }};
        return currentFinish()
    '''
    res = driver.execute_script(script)
    return res   #finished:True unfinished:percent

def judge():
    global res
    try:
        res = is_finished()

        # 解决弹窗检测
        topic_item = driver.find_element(By.XPATH, '//*[@id="playTopic-dialog"]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]')  # 随便选第一个选项
        dialog_test = driver.find_element(By.XPATH, '//*[@id="playTopic-dialog"]/div/div[1]/button/i')  # 关闭弹窗检测
        play_button = driver.find_element(By.XPATH, '//*[@id="playButton"]')
        #next_button = driver.find_element(By.XPATH, '//*[@id="nextBtn"]')
        topic_item.click()
        dialog_test.click()
        time.sleep(1)
        play_window = driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
        ActionChains(driver).move_to_element(play_window).perform()
        time.sleep(1)
        play_button.click()
    except Exception as e:
        pass






#定位到未看完课程小节号
def find_not_finished(Class_list):
    for i in Class_list:
        if Class_list[0]['finish'] == True:
            print(f"{Class_list[0]['unit']}小节已看完")
            Class_list.pop(0)
        else:
            print(f"已定位到没有看完小节，{Class_list[0]['unit']}")
            return Class_list[0]['unit']   #返回未观看课程的unit  如第一节课unit = 0.1
    return None




if __name__ == '__main__':
    #自动化登录
    # 绕过window.navigator.webdriver控件检测
    option = Options()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--disable-blink-features=AutomationControlled')

    driver = Chrome(options=option, service=ChromeService(ChromeDriverManager().install()))

    # 解决特征识别的代码
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    driver.execute_script(script)

    driver.get(url)

    cs = CrackSlider(driver)
    user = 'phone'
    passwd = 'password'

    while True:
        try:
            cs.login(user,passwd)
            time.sleep(2)
            if driver.current_url == url:   #没有跳转页面，说明验证没成功，登陆失败
                driver.refresh()
            else:
                break
        except Exception as e:
            driver.refresh()

    time.sleep(2)

    driver = cs.driver
    #点击进入课程页面
    find_class(driver,1)

    # 获取class列表
    #print(Class_list_init())
    Class_list = Class_list_init()[0]
    not_finished_list = Class_list_init()[1]
    #print(not_finished_list)

    #存放所有课程小节号的selenium元素列表
    all_units = class_unit = driver.find_elements(By.CLASS_NAME,"pl5.hour")
    # print(all_units)

    #定位且观看到未看完的课程
    if play_not_finished(all_units):
        sys.exit()




