import requests
from bs4 import BeautifulSoup

class QSBK:
    global stories
    stories = []
    def __init__(self, max_page):
        self.max_page = max_page
        self.page_index = 1
        self.url = 'https://www.qiushibaike.com/8hr/page/'

    def getPage(self):
        url =self.url+str(self.page_index)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='lxml')
        return soup

    def getStory(self,soup):
        tag = soup.find(name='div', attrs={'id': 'content-left'})
        content_list = tag.find_all('div', recursive=False)
        story = {}
        for item in content_list:
            if item.find(name='div', attrs={'class': 'thumb'}):
                continue
            else:
                author_name = item.find(name='div', attrs={'class': 'author clearfix'}).find('h2').text.strip()
                content = item.find(name='div', attrs={'class': 'content'})
                text = content.find('span').text.strip()
                thumb_up = item.find(name='div', attrs={'class': 'stats'}).find('span', class_="stats-vote").find(
                    'i').text.strip()
                comments = item.find(name='div', attrs={'class': 'stats'}).find('span', class_="stats-comments").find(
                    'i').text.strip()
                # print(author_name, text, thumb_up, comments)
                story = {'author_name':author_name,'text':text,'thumb_up':thumb_up,'comments':comments}
                global stories
                stories.append(story)
        return stories

    def getOneStory(self, stories):
        num = 0

        while True:
            Story = stories[num]

            print("发布人：%s \n 段子：%s \n 赞数：%s\t评论数：%s"%(Story['author_name'],Story['text'],Story['thumb_up'],Story['comments']))
            insert = input("回车查看下一个段子:")
            num +=1


    def start(self):
        print("正在读取糗事百科,按回车查看新段子，Q退出")
        while(self.page_index<=self.max_page):
            soup = self.getPage()
            stories = self.getStory(soup)
            self.page_index+=1
        self.getOneStory(stories)


spider = QSBK(max_page=3)
spider.start()





