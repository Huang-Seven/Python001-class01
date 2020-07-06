import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'
myurl = 'https://maoyan.com/films?showType=3'

header = {
    'Cookie':'_lxsdk_cuid=173100a7958c8-0f9865b106faca-31607402-13c680-173100a7959c8; uuid_n_v=v1; iuuid=C3C68980BC7711EAB07393F992BE3BBEA50C4C9E94554056B7C5AE82AB8A250D; webp=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173101ebcb1770-0dd2451d4b04c8-73236134-278385-173101ebcb281a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22173101ebcb1770-0dd2451d4b04c8-73236134-278385-173101ebcb281a%22%7D; _last_page=c_dmLad; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593701988,1593831315,1593831503,1593831791; __mta=45505947.1593701988734.1593831503175.1593831791975.6; _lxsdk=C3C68980BC7711EAB07393F992BE3BBEA50C4C9E94554056B7C5AE82AB8A250D; ci=20%2C%E5%B9%BF%E5%B7%9E; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593915642; __mta=45505947.1593701988734.1593831791975.1593915642662.7; latlng=22.3193039%2C114.16936109999999%2C1593915643475; _lxsdk_s=1731cc5f0d3-31f-2e8-0db%7C%7C4',
    'user-agent': user_agent}
response = requests.get(myurl,headers=header)
print(response.status_code)
print(response.cookies)
bs_info = bs(response.text,'html.parser')
movie_infos = []
for tags in bs_info.find_all('div',attrs={'class':'movie-hover-info'}):
    for atag in tags.find_all('div',attrs={'class':'movie-hover-title'}):
        for hover_tag in atag.find_all('span',attrs={'class':'hover-tag'}):
            movie_title = hover_tag.find_parent('div').get('title')
            if hover_tag.text == '类型:':
                movie_type = hover_tag.find_parent('div').text.strip().split('\n')[-1].strip()
            
            if hover_tag.text == '上映时间:':
                movie_online_time = hover_tag.find_parent('div').text.strip().split('\n')[-1].strip()
            hover_infos.append(hover_title,movie_type,movie_online_time)


# 通过 pandas 转csv，只存10个电影即可
df = pd.DataFrame(movie_infos[:10],columns=['movie-title', 'movie-type', 'movie-online-date'])
df.to_csv('./movie1.csv',encoding='utf8',index=False,header=False)