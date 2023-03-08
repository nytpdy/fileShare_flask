import  random
import os
import time
import datetime

#文件目录
FILE_DIR = 'D:/'

def  generate_verification_code( len ):
     ''' 随机生成6位的验证码 '''
     # 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
     # 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
     code_list  =  []
     for  i  in  range ( 10 ):  # 0-9数字
         code_list.append( str (i))
     for  i  in  range ( 65 ,  91 ):  # 对应从“A”到“Z”的ASCII码
         code_list.append( chr (i))
     for  i  in  range ( 97 ,  123 ):  #对应从“a”到“z”的ASCII码
         code_list.append( chr (i))
     myslice  =  random.sample(code_list,  len )   # 从list中随机获取6个元素，作为一个片断返回
     verification_code  =  ''.join(myslice)  # list to string
     return  verification_code


#时差
def diff():
    '''time diff'''
    starttime = datetime.datetime.now()
    time.sleep(10)
    endtime = datetime.datetime.now()
    print ("time diff: %d" % ((endtime-starttime).seconds))


#文件删除
def fileremove(filename, timedifference):
    '''remove file'''

    date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    print (date)

    now = datetime.datetime.now()
    print (now)

    print ('seconds difference: %d' % ((now - date).seconds))

    if (now - date).seconds > timedifference:
        if os.path.exists(filename):
            os.remove(filename)
            print ('remove file: %s' %filename)
        else:
            print ('no such file: %s' % filename)





if __name__ =='__main__':
    print(generate_verification_code(10))
    while True:
        ITEMS = os.listdir(FILE_DIR)
        NEWLIST = []
        for names in ITEMS:
            if names.endswith(".txt"):
                NEWLIST.append(FILE_DIR + names)
        # print NEWLIST

        for names in NEWLIST:
            print
            'current file: %s' % (names)
            fileremove(names, 10)

        time.sleep(10)