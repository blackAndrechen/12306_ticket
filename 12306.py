import re,requests,json,time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

start_station,end_station = '东莞','兴国'
#date = time.strftime("%Y-%m-%d")
dates = ['2018-02-03','2018-02-04']
sender = '2574759572@qq.com'#发件人
receiver = '980163660@qq.com'#收件人
pswd = 'lykovkuuuettebef'

def station_code(start_station,end_station):
	code_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.897'
	response = requests.get(code_url)
	stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
	station_dic = dict(stations)
	return station_dic[start_station],station_dic[end_station]


def search_tick(date): #查询余票
	url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
	response = requests.get(url).text
	json_data = json.loads(response)
	json_result = json_data['data']['result']
	result = []
	for i in json_result:
		result_single = i.split('|')
		result_dict = {'日期':date,
		'车次':result_single[3],
		'无座':result_single[-11],
		'硬座':result_single[-8],
		'软座':result_single[-13],
		'软卧':result_single[-14],
		'硬卧':result_single[-7]}
		result.append(result_dict)
	return result

def send_email(str):
    message = MIMEText(str,'plain','utf-8')
    message['From'] = Header('抢票提示','utf-8').encode()
    message['To'] = Header('you','utf-8').encode()
    message['Subject'] = Header('12306余票提示','utf-8').encode()
    smtp_obj = smtplib.SMTP_SSL('smtp.qq.com',465)
    smtp_obj.login(sender,pswd)
    smtp_obj.sendmail(sender,[receiver],message.as_string())
    smtp_obj.quit()

from_station,to_station = station_code(start_station,end_station)
search_result = []
for date in dates:
	search_result =search_result + search_tick(date)

str_tick = ''	
for m in search_result:
	keys = m.keys()
	for key in keys:
		if m[key] == '有':
			str_tick = str_tick + str(m)
if len(str_tick) >= 0:
	send_email(str_tick)

