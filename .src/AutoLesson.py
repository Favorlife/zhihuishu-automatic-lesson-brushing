# -*- coding: utf-8 -*-
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://passport.zhihuishu.com/login'


class AutoLessons():
    def __init__(self):
        self.url = 'https://passport.zhihuishu.com/login'
        # 自动化登录
        # 绕过window.navigator.webdriver控件检测
        option = Options()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = Chrome(options=option, service=ChromeService(ChromeDriverManager().install()))

        # 解决特征识别的代码
        script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        self.driver.execute_script(script)

        self.driver.get(url)


    def login(self, user, passwd):
        user, passwd = user, passwd
        cs = CrackSlider(self.driver)
        #傻瓜式登录+人机验证，失败则刷新重来（有待改善）
        while True:
            try:
                cs.ZHSlogin(user, passwd)
                time.sleep(2)
                if self.driver.current_url == url:  # 没有跳转页面，说明验证没成功，登陆失败
                    self.driver.refresh()
                else:
                    break
            except Exception as e:
                self.driver.refresh()
        time.sleep(2)
        self.driverdriver = cs.driver
    #定位到课程*********************************************************************************
    def find_class(self, class_name):   #class_num是平台里面共享学分课从上到下的顺序（由1开始）
        # 定位到“我的学堂”
        wait = WebDriverWait(self.driver, 10)
        my_classes = wait.until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, '//*[@id="headerMain"]/ul/li[4]/a')))
        my_classes.click()
        time.sleep(3)
        # 关闭‘切换身份提醒’,一般要点两次
        try:
            close_tip = wait.until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, '//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]')))
            '''
            '//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]'   这是路人账号关闭提示路径
            '//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]'   这是学生账号关闭提示路径
            '''
            close_tip.click()
            close_tip.click()

        except Exception as e:
            pass

        # while True:
        #     try:
        #         close_tip = wait.until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, '//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]')))
        #         '''
        #         '//*[@id="student-page"]/div[5]/div/div/div[2]/div[2]'   这是路人账号关闭提示路径
        #         '//*[@id="student-page"]/div[4]/div/div/div[2]/div[2]'   这是学生账号关闭提示路径
        #         '''
        #         close_tip.click()
        #         close_tip.click()
        #         break
        #     except Exception as e:
        #         self.driver.refresh()
        #         time.sleep(2)
        # 定位到课程

        f_url = self.driver.current_url
        while True:
            try:
                time.sleep(0.5)
                classelem = self.driver.find_element(By.XPATH, f'//*[@id="sharingClassed"]//*[contains(text(), "{class_name}")]')
                classelem.click()
                time.sleep(0.5)
                if self.driver.current_url == f_url:
                    continue
                else:
                    break
            except Exception as e:
                self.driver.refresh()

        time.sleep(4)
        # 关闭诚信学习警告-我知道了  和 学前必读
        while True:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[6]/div/div[3]/span/button').click()
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[7]/div[2]/div[1]/i').click()
                break
            except Exception as e:
                self.driver.refresh()
                time.sleep(2)

    # 自动播放视频*******************************************************************************
    def play(self):
        while True:
            try:
                # 定位到播放按钮
                time.sleep(2)
                play_window = self.driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
                ActionChains(self.driver).move_to_element(play_window).perform()  # 防止进度条消失
                play_button = self.driver.find_element(By.XPATH, '//*[@id="playButton"]')
                next_button = self.driver.find_element(By.XPATH, '//*[@id="nextBtn"]')

                play_button.click()

                # 写入更改倍速的js
                speed_script = '''
                function changeSpeed(){
                var x = document.querySelector('.speedTab10');
                x.setAttribute('rate','16.0');
                }
                changeSpeed()
                '''
                self.driver.execute_script(speed_script)

                # 点击更改倍速为 1.25， 实现x16倍速
                time.sleep(0.5)
                speed_button = self.driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[8]/span')
                ActionChains(self.driver).move_to_element(speed_button).perform()
                speed_125 = self.driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[10]/div[8]/div/div[2]')
                speed_125.click()
                return
            except Exception as e:
                self.driver.refresh()
                time.sleep(1)
                print('play error, refresh successful')

    def play_not_finished(self, all_units):
        index = self.find_not_finished(self.Class_list)
        if index == None:
            print("You've finished watching your online course.")
            return True
        while index != None:
            index = self.find_not_finished(self.Class_list)
            print(f'准备播放{index}')

            # 跳转到未完成的课程
            while True:
                try:
                    if all_units[0].text == index:  # 如果按顺序找到了没有播放的课程小节号，则点击跳转
                        time.sleep(1)
                        all_units[0].click()  # 点击跳转
                        break
                    else:
                        print('locating')
                        all_units.pop(0)
                except:
                    self.driver.refresh()
                    time.sleep(2)


            # 播放
            self.play()
            # 检测是否播放完成(另起一个线程，在播放过程中循环检测，直到检测为finished则结束)
            global res
            res = False  # 存放返回值
            while True:
                self.judge()
                temp_res = res
                if res != True:
                    print(f'continue{index}:{res}', end='-->-->')
                    time.sleep(6)
                    self.judge()
                    if (temp_res == res) and res != True:  # 6秒后进度不变 可能是结束了也可能是暂停了
                        print('进度条没变化，再次点击播放键')
                        # 重新播放
                        while True:
                            try:
                                time.sleep(1)
                                play_button = self.driver.find_element(By.XPATH, '//*[@id="playButton"]')
                                play_window = self.driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
                                ActionChains(self.driver).move_to_element(play_window).perform()
                                time.sleep(1)
                                play_button.click()
                                break
                            except:
                                self.driver.refresh()
                                time.sleep(2)

                elif res == True:
                    print(f'end{index}')
                    self.Class_list.pop(0)
                    all_units.pop(0)
                    break
        print("You've finished watching your online course.")
        return True

    # 获取当前课程的所有课的列表
    def Class_list_init(self):
        # 通过js返回
        # 课程列表
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

        all_list = self.driver.execute_script(script1)  # return 2 array
        # all_list[0]:  example: 'finish': True/faulse, 'time': '00:07:11', 'title': '引言', 'unit':0.1
        # all_list[1]:  not finished class
        return all_list

    # 判断是否看完当前课程
    def is_finished(self):
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
        res = self.driver.execute_script(script)
        return res  # finished:True unfinished:percent

    def judge(self):
        global res
        try:
            res = self.is_finished()

            # 解决弹窗检测
            topic_item = self.driver.find_element(By.XPATH, '//*[@id="playTopic-dialog"]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]')  # 随便选第一个选项
            dialog_test = self.driver.find_element(By.XPATH, '//*[@id="playTopic-dialog"]/div/div[1]/button/i')  # 关闭弹窗检测
            play_button = self.driver.find_element(By.XPATH, '//*[@id="playButton"]')
            #next_button = driver.find_element(By.XPATH, '//*[@id="nextBtn"]')
            topic_item.click()
            dialog_test.click()
            time.sleep(1)
            play_window = self.driver.find_element(By.XPATH, '//*[@id="vjs_container"]/div[8]')
            ActionChains(self.driver).move_to_element(play_window).perform()
            time.sleep(1)
            play_button.click()
        except Exception as e:
            pass

    #定位到未看完课程小节号
    def find_not_finished(self, Class_list):
        while Class_list != None:
            if Class_list[0]['finish'] == True:
                print(f"{Class_list[0]['unit']}小节已看完")
                Class_list.pop(0)
            else:
                print(f"已定位到没有看完小节，{Class_list[0]['unit']}")
                return Class_list[0]['unit']   #返回未观看课程的unit  如第一节课unit = 0.1



        # for item in Class_list:
        #     if item['finish'] == True:
        #         print(f"{item['unit']}小节已看完")
        #         Class_list.pop(0)
        #     else:
        #         print(f"已定位到没有看完小节，{item['unit']}")
        #         return item['unit']   #返回未观看课程的unit  如第一节课unit = 0.1
        return None

    def auto(self, user, passwd, class_num):
        self.login(user, passwd)
        self.find_class(class_num)
        # 获取class列表
        self.Class_list = self.Class_list_init()[0]
        self.not_finished_list = self.Class_list_init()[1]
        # 存放所有课程小节号的selenium元素列表
        self.all_units = self.driver.find_elements(By.CLASS_NAME, "pl5.hour")
        # 定位且观看到未看完的课程
        if self.play_not_finished(self.all_units):
            sys.exit()
        self.driver.find_element(By.CLASS_NAME,'')






