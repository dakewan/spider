import requests,os
from bs4 import BeautifulSoup


base_url = 'http://www.mzitu.com/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

r1 = requests.get(url=base_url)
# print(r1.text)
soup = BeautifulSoup(r1.text,features='lxml')
# 获取所有套图链接
tags = soup.find(name='ul',id="pins").find_all('li')
url_list = []
for tag in tags:
    url = tag.find('span').find('a').get('href')
    # print(img_url)
    url_list.append(url)

for url in url_list:
    # 获取套图链接信息
    r2 = requests.get(url=url)
    soup = BeautifulSoup(r2.text,features='lxml')

    title = soup.find('h2',class_='main-title').text.strip()
    # img_url = soup.find('div',class_='main-image').find('img').get('src')
	# 获取套图总张数
    num = int(soup.find('div',class_='pagenavi').find_all('span')[-2].text)
	# 保存路径文件夹
    path = os.path.join(BASE_DIR,title)
    # print(path)
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
	#循环获取各图片URL
    for i in range(1,num+1):
        url_new = "%s/%s"%(url,i)
        r3 = requests.get(url=url_new)
        soup = BeautifulSoup(r3.text,features='lxml')
        img_url = str(soup.find('div',class_='main-image').find('img').get('src'))
		# 添加请求头应对图片防盗链
        r4 = requests.get(url=img_url,
                    headers={'Referer':url_new})
        # print(type(img_url))
        dict = img_url.rsplit('/',maxsplit=1)
        file_name = os.path.join(path,dict[1])
        # print(file_name)
        with open(file_name,'wb') as f:
            f.write(r4.content)



