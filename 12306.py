# -*-coding:utf-8-*-
'''命令行查看火车票
Usage:12306 [-hgdztka] <from> <to> <date>

Options:
 -h, --help 显示帮助菜单
 -g         高铁
 -d         动车
 -z         直达
 -t         特快
 -k         快速
 -a         全部车次

Example:
    12306 -g 北京 上海 20161220
'''

import requests
from prettytable import PrettyTable
from docopt import docopt
from colorama import init, Fore

from stations import stations


init()

def get_json(url):
    response = requests.get(url, verify=False)
    return response.json()[u'data']

def judge_can_use(from_station, to_station):
    if from_station is None:
        return '错误的出发站'
    elif to_station is None:
        return '错误的到达站'

class TransData(object):

    option_available = {}
    def __init__(self, needtrains, option):
        """查询火车班次的所有数据
        : param needtrains: 关于火车班次信息的一个列表,每个火车班次是一个字典
        : param option： 查询选项，比如高铁，动车
        """
        self.need_trains = needtrains
        self.option = option[1:]

    def pring_data(self, data_list):
        row = PrettyTable()
        row.field_names = ['车次', '车站', '出发日期', '时间', '历时', '商务座', '二等座', '一等座', '硬卧',
                           '软卧', '硬座', '软座', '无座']
        for x in data_list:
            row.add_row(x)
        print row



    def get_use_information(self):
        self.data_list = []
        for one_information in self.need_trains:
            self.useful_data = one_information[u'queryLeftNewDTO']
            tran_type = self.useful_data[u'station_train_code'][0].lower()
            if not self.option or tran_type in self.option or self.option is 'a':
                self.useful_data_list = []
                self.useful_data_list.append(self.useful_data[u'station_train_code'])
                self.useful_data_list.append('\n'.join([Fore.GREEN + self.useful_data[u'from_station_name'] + Fore.RESET,
                                                        Fore.RED + self.useful_data[u'to_station_name'] + Fore.RESET]))
                # self.useful_data_list.append(self.useful_data[u'end_station_name'])
                self.useful_data_list.append(self.useful_data[u'start_train_date'])
                self.useful_data_list.append('\n'.join([Fore.GREEN + self.useful_data[u'start_time'] + Fore.RESET,
                                                        Fore.RED + self.useful_data[u'arrive_time'] + Fore.RESET]))
                # self.useful_data_list.append(self.useful_data[u'arrive_time'])
                self.useful_data_list.append(self.useful_data[u'lishi'])
                self.useful_data_list.append(self.useful_data[u'swz_num'])  # 商务座
                self.useful_data_list.append(self.useful_data[u'ze_num'])  # 二等座
                self.useful_data_list.append(self.useful_data[u'zy_num'])  # 一等座
                self.useful_data_list.append(self.useful_data[u'yw_num'])  # 硬卧
                self.useful_data_list.append(self.useful_data[u'rw_num'])  # 软卧
                self.useful_data_list.append(self.useful_data[u'yz_num'])  # 硬座
                self.useful_data_list.append(self.useful_data[u'rz_num'])  # 软座
                self.useful_data_list.append(self.useful_data[u'wz_num'])  # 无座
            self.data_list.append(self.useful_data_list)
        return self.data_list

    def start_open(self):
        information = self.get_use_information()
        self.pring_data(information)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>'][:4] + '-' + arguments['<date>'][4:6] + '-' + arguments['<date>'][6:]
    # print date
    if judge_can_use(from_station, to_station):
        print judge_can_use()
        exit()
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}' \
          '&purpose_codes=ADULT'.format(date, from_station, to_station)
    # print url
    tran_data_list = get_json(url)  # list
    option = ''.join([key for key, value in arguments.items() if value is True])
    trandata = TransData(tran_data_list, option)
    final_data = trandata.start_open()

