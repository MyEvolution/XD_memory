# -*- coding: utf-8 -*-

import oss2

import traceback


PREFIX = 'https://'



    # ossinfo { # ossinfo ={ACCESS_KEY_ID,ACCESS_KEY_SECRET，ENDPOINT，BUCKETNAME_XLS}
    # timerange 时间毫秒值
    # urlload 文件目录
def find_oss_file(ossinfo, urlload):
    result = {}
    urlDict = {}
    urlList = []
    try:
        auth = oss2.Auth(ossinfo['ACCESS_KEY_ID'], ossinfo['ACCESS_KEY_SECRET'])
        bucket = oss2.Bucket(auth, ossinfo['ENDPOINT_OUT'], ossinfo['BUCKETNAME_XLS'])
        for filename in oss2.ObjectIterator(bucket, prefix='%s/'%urlload):
            sourceURL = PREFIX + ossinfo['BUCKETNAME_XLS'] + '.' + ossinfo['ENDPOINT_OUT'] +'/'+ filename.key
            sourceTime = filename.last_modified
            if sourceTime in urlDict.keys():
                    #最多保证10个相同时间的路径不覆盖
                sourceTime += 0.1
            urlDict[sourceTime] = sourceURL
        newurl = sorted(urlDict.items(), key=lambda asd: asd[0], reverse=True)
        for u in newurl:
            urlList.append(u[1])
        result['fileurl'] = urlList
        result['errorcode'] = 0
        return result
    except Exception:
        result['errorcode'] = -1
        result['errortext'] = '%s_%s' % (traceback.print_exc(), Exception)
        return result
if __name__ == "__main__":
    print(find_oss_file({'ACCESS_KEY_ID':'LTAIp30IrNg9U9MX','ACCESS_KEY_SECRET':'c4L39uBdzkDRrFuQ8A2RBcHJ9bpkbB','ENDPOINT_OUT':'oss-cn-beijing.aliyuncs.com',
                         'BUCKETNAME_XLS':'evolution-video'},'user1'))