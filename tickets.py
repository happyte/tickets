# -*- coding:utf-8 -*-

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""

from docopt import docopt
from staions import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

init()

def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_staion = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.' \
          'from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.\
        format(date, from_station, to_staion)
    response = requests.get(url, verify=False)
    options = ''.join([key for key, value in arguments.items() if value is True])
    TransCollection(response.json()['data'], options).pretty_print()

class TransCollection:
    header = '车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        self.availavle_trains = available_trains
        self.options = options

    def _get_duration(self, train_data):
        duration = train_data.get('lishi').replace(':', '小时')+'分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for train in self.availavle_trains:
            train_data = train['queryLeftNewDTO']
            train_number = train_data['station_train_code'][0].lower()   # 开头转换成小写
            if not self.options or train_number in self.options:
                train = [
                    train_data['station_train_code'],              # 车次
                    '\n'.join([Fore.GREEN+train_data['from_station_name']+Fore.RESET,    # 车站
                               Fore.RED+train_data['to_station_name']+Fore.RESET]),
                    '\n'.join([Fore.GREEN+train_data['start_time']+Fore.RESET,           # 车站
                               Fore.RED+train_data['arrive_time']+Fore.RESET]),
                    self._get_duration(train_data),                # 历时
                    train_data['zy_num'],                          # 一等座
                    train_data['ze_num'],                          # 二等座
                    train_data['rw_num'],                          # 软卧
                    train_data['yw_num'],                          # 硬卧
                    train_data['yz_num'],                          # 硬座
                    train_data['wz_num'],                          # 无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

if __name__ == '__main__':
    cli()