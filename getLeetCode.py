#coding:utf-8
import urllib2
import urllib
import cookielib

mydir = r'/home/jimmy/pythonTest/'
myhost = r'https://leetcode.com'

cj = cookielib.CookieJar()
cookies = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookies)
opener.open('https://leetcode.com')

csrftoken = ''
for ck in cj:
    csrftoken = ck.value

login = 'zkdnfcf'
password = 'zkdnfcf386132'

values = {'csrfmiddlewaretoken':csrftoken,'login':login,'password':password,'remember':'on'}
values = urllib.urlencode(values)
headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6',
        'Origin':'https://leetcode.com',
        'Referer':'https://leetcode.com/accounts/login/'
        }

request = urllib2.Request("https://leetcode.com/accounts/login/",values,headers=headers)
url = opener.open(request)
page = url.read()
print page

def saveCode(code,title):
    global mydir
    f = open(mydir+title+'.cpp','w')
    f.write(code)

def downloadACcode(refer,codeadd,title):
    global headers
    global opener
    global myhost
    headers['Referer'] = refer
    request = urllib2.Request(codeadd,headers=headers)
   # print 'codeadd' + codeadd + 'refer' + refer + 'title'+title + '\n'
    url = opener.open(request)
    allAc = url.read()
    tar = "storage.put('cpp',"
    index = allAc.find(tar,0)
    start = allAc.find('class Solution',index)
    finish = allAc.find("');",start)
    code = allAc[start:finish]
    toCpp = {'\u000D':'\n','\u000A':'','\u003B':';','\u003C':'<','\u003E':'>','\u003D':'=','\u0026':'&','\u002D':'-','\u0022':'"','\u0009':'\t','\u0027':"'",'\u005C':'\\'}

    for key in toCpp.keys():
        code = code.replace(key,toCpp[key])

    print code
    saveCode(code,title)

def findCode(address,title):
    global headers
    global opener
    global myhost
    #print 'address' + address + 'title' + title

    print title
    headers['Referer'] = address
    address += 'submissions/'
    print 'now is dealing' + address + ':' + title

    request = urllib2.Request(address,headers=headers)
    url = opener.open(request)
    allSubmit = url.read()
    print 'start';
    print allSubmit
    tar = 'status-accepted'
    index = allSubmit.find(tar,0)
    start = allSubmit.find('href="',index)
    finish = allSubmit.find('">',start)
    print start,finish
   # print 'address:' + address + '    title:'+title + '\n' + myhost+allSubmit[start+6:finish]
    downloadACcode(address,myhost+allSubmit[start+6:finish],title)

def findAc(page):
    index = 0
    while 1:
        index = page.find('class="ac"',index)
        if index != -1:
            index += 1
            start = page.find('<a href="',index)
            finish = page.find('">',start)
            tmpfinish = page.find('<',finish)
            title = page[finish+2:tmpfinish]
            print title
            findCode(myhost+page[start+9:finish],title)
        else:
            break
findAc(page)

#g = opener.open('https://oj.leetcode.com/submissions/')
#print g.read()
