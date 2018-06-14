# -*-encoding:utf-8-*-
import web
import os
import getOssFiles


urls = (
    '/', 'xd_memory',
    '/xd_memory','xd_memory',
    '/xdmemory','xd_memory'
)
app = web.application(urls, globals())
render=web.template.render('template')
class xd_memory:
    def GET(self):
        inf = web.input(location="",road="true",map="")
        location = inf.location
        road=inf.road

        map = inf.map
        if location=="":
            xdfile = []
            _f = open("./XD", "r", encoding='UTF-8')
            line = _f.readline()[0:-1]
            while line:
                files = line.split(' ')
                xdfile.append(files)
                line = _f.readline()[0:-1]
                # for ename,lat,lng,detail in xdfile:
                # print(ename,lat,lng,detail)
            cookie = web.cookies(can_you_upload="no_i_can_not",username="anonymous")
            username = cookie.username
            cookie = cookie.can_you_upload
            if cookie == "yes_i_can":
                web.setcookie('can_you_upload','yes_i_can',10800)
                web.setcookie('username',username)
                if map=="baidu":
                    return  render.index_baidu(xdfile,1,username)
                else:
                    return render.index(xdfile,1,road,username)
            else:
                if map=="baidu":
                    return  render.index_baidu(xdfile,0,username)
                else:
                    return render.index(xdfile,0,road,username)
        else:
            ossinfo = {'ACCESS_KEY_ID':'your_id','ACCESS_KEY_SECRET':'your_key','ENDPOINT_OUT':'oss-cn-beijing.aliyuncs.com',
                         'BUCKETNAME_XLS':'your_bucket'}
            files_result = getOssFiles.find_oss_file(ossinfo,location)
            if files_result['errorcode'] == 0:
                cookie = web.cookies(can_you_upload="no_i_can_not",username="anonymous")
                username = cookie.username
                cookie = cookie.can_you_upload
                if cookie == "yes_i_can":
                    web.setcookie('can_you_upload', 'yes_i_can', 10800)
                    web.setcookie('username',username)
                    return render.video(files_result['fileurl'],location,1,username)
                else:return render.video(files_result['fileurl'],location,0,username)
    def POST(self):
        up = web.input(username="",password="")
        username = up.username
        if   up.password=="fuckTheW0rld":
            web.setcookie('can_you_upload','yes_i_can',10800)
            web.setcookie('username',username,10800)
        web.seeother('./xdmemory')

def run():
    app = web.application(urls, globals())
    app.run()
if __name__ == '__main__':

    run()
