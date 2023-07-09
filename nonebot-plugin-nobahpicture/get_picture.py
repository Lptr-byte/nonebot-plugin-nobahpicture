import os

import requests


class GetPicture():
    def __init__(self, pic_num: int = 1, user_tag: str = '', size: str = 'original', save: bool = False):
        self.pic_num = pic_num  #需要获取的图片数量
        #Ba Tag
        self.tag = [
            ['BlueArchive', '碧蓝档案', '蔚蓝档案']     #等有日语输入法再加tag
        ]
        self.user_tag = user_tag
        self.size = size
        self.save = save

    def get_picture(self):
        #请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Referer': 'www.pixiv.net',
            'Content-Type': 'application/json'
        }
        #使用POST请求获取网页返回的json数据
        url = 'https://api.lolicon.app/setu/v2'
        #如果用户有指定tag，则添加tag
        if len(self.user_tag):
            self.tag.append([self.user_tag])
        payload = {'r18': 0, 'num': self.pic_num, 'tag': self.tag, 'size': self.size, 'exCludeAI': False}
        r = requests.post(url, json=payload, headers=headers).json()
        #将图片url保存至列表
        res_url = []
        for i in range(1, self.pic_num + 1):
            res_url.append(r['data'][i - 1]['urls'][self.size])

        #下载图片并保存到本地
        if self.save:
            if not os.path.isdir('./pics'):
                os.mkdir('./pics')
            for i in range(1, self.pic_num + 1):
                with open('./pics/{name}.{ext}'.format(name=r['data'][i - 1]['title'],
                                                    ext=r['data'][i - 1]['ext']), mode='wb') as f:
                    res = requests.get(r['data'][i - 1]['urls'][self.size], headers=headers)
                    f.write(res.content)

        return res_url
