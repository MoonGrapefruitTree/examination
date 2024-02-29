import selenium.webdriver as webdriver
from selenium.webdriver.support.select import Select
import sys

opt = webdriver.ChromeOptions()   # 创建chrome对象
opt.add_argument('headless')   # 把chrome设置成wujie面模式，不论windows还是linux都可以，自动适配对应参数
opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/88.0.4324.96 Safari/537.36")
driver = webdriver.Chrome(options=opt)    # 指定chrome驱动程序位置和chrome选项
driver.implicitly_wait(3)  # 设置等待加载完成在继续
'''
这是中国银行外汇牌价网站：https://www.boc.cn/sourcedb/whpj/
请使用python3 和 selenium库写一个程序，实现以下功能：

输入：日期、货币代号
输出：该日期该货币的“现汇卖出价”

示例
python3 yourcode.py 20211231 USD
输出：636.99

该日期有很多个价位，只需要输出任意一个时间点的价位即可。
货币代号为USD、EUR这样的三位英文代码，请参考这里的标准符号：https://www.11meigui.com/tools/currency
'''


# 用于获得中文货币名称和英文缩写的映射字典  但是11meigui.com 网站上货币中文名称和中国银行货币名称并不一致，不能直接使用。
def get_currency_dictionary_web():
    url = 'https://www.11meigui.com//tools//currency' # 字典网页
    driver.get(url)
    tables = driver.find_elements('xpath', '//*[@class="container currency"]/table/tbody/tr[2]/td/table')
    currency_dict = {}
    for table in tables:
        trs = table.find_elements('xpath', './tbody/tr')
        for i in range(len(trs) - 2):
            tds = trs[i + 2].find_elements('xpath', './td')
            currency_dict[tds[-2].text] = tds[1].text  # 储存英文简写和中文名称的对应关系
    return currency_dict


# 手动构建货币中文名称和英文简写的对照字典。
def get_currency_dictionary():
    # 这里手动敲错键和值了，后面转换下
    currency_dict = {'英镑': 'GBP', '港币': 'HKD', '美元': 'USD', '瑞士法郎': 'CHF', '新加坡元': 'SGD', '瑞典克朗': 'SEK',
                     '丹麦克朗': 'DKK', '挪威克朗': 'NOK', '日元': 'JPY', '加拿大元': 'CAD', '澳大利亚元': 'AUD', '欧元': 'EUR',
                     '澳门元': 'MOP', '菲律宾比索': 'PHP', '泰国铢': 'THP', '新西兰元': 'NZD', '韩元': 'WON', '卢布': 'SUR',
                     '林吉特': 'MYR', '新台币': 'TWD', '西班牙比塞塔': 'ESP', '意大利里拉': 'ITL', '荷兰盾': 'NLG', '比利时法郎': 'BEF',
                     '芬兰马克': 'FIM', '印尼卢比': 'IDR', '巴西里亚尔': 'BRC', '阿联酋迪拉姆': 'DHS', '印度卢比': 'INR', '南非兰特': 'ZAR',
                     '沙特里亚尔': 'SAR', '土耳其里拉': 'TRL'}
    currency_dict = dict(zip(currency_dict.values(), currency_dict.keys()))
    return currency_dict


def answer(currencyName, Date):
    url = 'https://www.boc.cn/sourcedb/whpj/'  # 数据网页
    driver.get(url)
    # 选择货币类型
    select = driver.find_elements('xpath', '//*[@id="pjname"]')[0]
    Select(select).select_by_visible_text(currencyName)
    try:
        # 选择起始时间
        Date = Date[0:4] + '-' + Date[4:6] + '-' + Date[6:8]
        date_erect = driver.find_elements('xpath', '//*[@id="erectDate"]')[0]
        date_erect.click()
        date_erect.send_keys(Date)
        # 选择结束时间
        date_erect = driver.find_elements('xpath', '//*[@id="nothing"]')[0]
        date_erect.click()
        date_erect.send_keys(Date)
    except:
        print("输入时间不合理")
    # 查询
    try:
        Query = driver.find_elements('xpath', '//*[@class="search_btn"]')[1]
        Query.click()
        # 从新页面获得价位。打印第一条数据的现汇买入价格
        data = driver.find_elements('xpath', '//*[@class="BOC_main publish"]/table/tbody/tr[2]/td')
        print(data[1].text)
    except:
        print("查询失败")


if __name__ == '__main__':
    date, currency_name = str(sys.argv[1]), str(sys.argv[2])
    currency_dict = get_currency_dictionary()
    try:
        currency_name = currency_dict[currency_name]
    except:
        print("没有对应货币")
    answer(currency_name, date)