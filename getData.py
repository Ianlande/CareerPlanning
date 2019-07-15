'''
    爬虫爬数据
    
    created by: longyucheng
    2019/6/28
'''
import re
import copy
import time
import random
import csv
import urllib.request
import urllib.parse

dataNum = 10000    # 需要爬的数据量
topic_num = 52  # 需要作答的题目数
ans_num = 5     # 每道题的选项数目
url_path = "http://www.zhiyeguihua.com/ceping/Report/"      # 网站
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"   # 用于伪装的用户
csvPath = 'data.csv'

'''
    随机生成数据, 这些数据将会被输入网站并获取结果
    数据用一个list表示, 输入题目题数和每道题的选项数
    程序原则上是生成伪随机数, 但这是允许的, 因为真实情况下的问卷调查也是符合正太分布的伪随机
'''
def generateData(topic_num, ans_num):
    data = []
    for each_topic in range(topic_num):
        data.append(random.randint(0, ans_num-1))   # ans_num-1因为0-4是5个数
    return data

# 使用正则表达式从获取的数据中提取需要的数据
def searchData(html):
    result = {}
    feature = ['社会交际', '安全感', '舒适', '成就感', '管理', '人际关系', '美感', '经济报酬', '利他主义', '追求新意', '独立性', '社会声望', '智力刺激']
    
    sec_start = re.search(r"你的测试结果是", html).span()
    sec_stop = re.search(r"<h3>描述: </h3>", html).span()
    sec = html[sec_start[0] : sec_stop[-1]]
    
    for each in feature:
        temp = re.findall(str(each + r"：\d+"), sec)
        result[each] = int(re.findall(r"\d+", temp[0])[0])  # findall返回一个list, list中只有一个str元素, 需要转换类型        
        
    return result
    
# 爬虫: 将生成的input输入网站并获取网站数据
def CrawlData(topic_num, ans_num, url_path, userAgent):
    
    # ======================== 生成输入数据 ========================
    input = generateData(topic_num, ans_num)
    output = []
    
    # ======================== 转成输入格式 ========================
    data = {}
    data['cid'] = 19
    data['authcode'] = {}
    for each in range(len(input)):
        temp_index = 'opts[' + str(625 + each) + ']'
        data[temp_index] = input[each]
    #print(data)
    data = urllib.parse.urlencode(data).encode('utf-8')
    #print(data)
    
    # ======================== 爬数据 ========================
    req = urllib.request.Request(url_path, data)
    req.add_header('User-Agent', userAgent)
    
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    #print(html)
    
    # ======================== 转成输出格式 ========================
    result = searchData(html)
    ans = sorted(result.items(), key = lambda x:x[1], reverse = True)
    # 转str类型才能存入csv文件
    for each in input:
        output.append(str(each))
    output.append(ans[0][0])
    
    return output
    
# 追加数据
def addData(data, path):
    ls = []
    ls.append(data)
    with open(path, "a+", newline = '') as file:
        csv_file = csv.writer(file)
        csv_file.writerows(ls)

data = []
for each in range(dataNum):
    eachData = CrawlData(topic_num, ans_num, url_path, userAgent)
    #print(eachData)
    addData(eachData, csvPath)
    time.sleep(1)
    print('已处理第', each+1, '个数据')


