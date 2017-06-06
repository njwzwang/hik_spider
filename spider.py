import requests
import re
from config import *
from requests.packages import urllib3

urllib3.disable_warnings()


def get_status_response(ip_addr):
    url = 'https://' + ip_addr + ':2004/web/dynamic.php'
    data = dict(ref='/header', autostart=0, target='refreshAlarm', r=0)

    try:
        response = requests.get(url, params=data, verify=False)
        response.raise_for_status()
        #print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)


def format_status(text):
    result = re.search('xml.*?([\u4e00-\u9fa5]+).*?dynamic_results', text, re.S)
    old = re.search('index.php.*?(\w+).*?script', text, re.S)

    if result:
        return result.group(1)
    if old:
        return old.group(1)
    else:
        return None


def main():
    print('Getting status')
    for ip_addr in IP_LISTS:
        response = get_status_response(ip_addr)
        if format_status(response) == '系统正常':
            print(ip_addr + ':' + format_status(response))
        elif format_status(response) == '系统异常':
            print(ip_addr + ':' + format_status(response))
        elif format_status(response) == 'requirelogin':
            print(ip_addr + ':' + 'Web Version Too Low')
        else:
            print(ip_addr + ':' + response)


if __name__ == '__main__':
    main()
