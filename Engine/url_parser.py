import re
from urllib import parse
# 这类词加分减分
# 可以把这些url分词排序然后认为判断加入消极还是积极
NEG_WORDS = ['user', 'list', 'author', 'comment','writer']
POS_WORDS = ['article', 'blog', 'details', 'question']
# 参考https://help.aliyun.com/document_detail/65096.html  
# 还要记住匹配的时候不能区分大小写，同时匹配的时候也仅仅需要匹配url的最后四位就可以了
# 这类词一票否决
FILE_WORDS = ['.gif','.png','.bmp','.jpeg','.jpg', '.svg',
              '.mp3','.wma','.flv','.mp4','.wmv','.ogg','.avi',
              '.doc','.docx','.xls','.xlsx','.ppt','.pptx','.txt','.pdf',
              '.zip','.exe','.tat','.ico','.css','.js','.swf','.apk','.m3u8','.ts']

# 还有就是如果包含很长一串数字的一般都是内容界面
# 不应该是各种文件名的后缀
def is_static_url(url):
    '''
    
    '''
    for w in FILE_WORDS:
        if w in url[-5:]:
            return True

    return False

# 暂时不用
# 这个有点麻烦，先用别人实现的，自己后面再参考着来实现在我这种应用场景下的判断
def is_content_url(url, threshold=0.4):
    '''
    判断一个url是否为内容界面，而不是列表界面或者主页又或者用户页等;
    param:
        url:传入的url;
        threshold:决定是否为内容界面的阈值;
    return:
        bool;
    '''
    suffix = re.findall('[a-z]+', (url[-5:]).lower())
    if len(suffix) != 0:
        if suffix[-1] in FILE_WORDS:
            return False
    score = 0
    if re.match("[0-9]"*10, url, flags=0) != None:
        score += 30
    for w in NEG_WORDS:
        if w in url:
            score -= 10
    for w in POS_WORDS:
        if w in url:
            score += 15
    if(score/(len(url)*2) >= threshold):
        return True
    else:
        return False

# 暂时不用
STOP_WORD = "javascript:"
def url_filter(urls):
    cleaned_urls = []
    for url in urls:
        if is_static_url(url):
            continue
        if STOP_WORD in url.lower():
            continue
        cleaned_urls.append(url)
    return cleaned_urls
                