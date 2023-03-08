# 文件操作
import pandas as pd
import csv
import random
import os


def openfile(username):
    userpath = os.getcwd() + '\data' + '\\' + username + '.csv'
    if not os.path.exists(userpath):
        with open(userpath, 'w') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(["文件收藏"])
    df = pd.read_csv(userpath, encoding="gbk", header=None, skiprows=0, sep='\t')
    return df


def savefile(username, data):
    userpath = os.getcwd() + '\data' + '\\' + username + '.csv'
    data.to_csv(userpath, index=False, header=False, encoding='GBK')


def writefile(username, data):
    df = openfile(username)
    df.loc[len(df.index)] = data
    savefile(username, df)
    # print(data, "write")
    return '写入成功'


def deletefile(username, data):
    df = openfile(username)
    for i in range(len(df)):
        if str(df[0][i]) == data:
            df.drop(i, inplace=True)
    savefile(username, df)


def collection(username: object, data: object) -> int:
    """

    :rtype: object
    """
    df = openfile(username)
    if data in df.values:
        return 1
    return 0

    # if __name__ == '__main__':
    # print(df)
    # df[0][1] = "玩的啥环境发生恐动环监控"
    # print(df[0][1])
    # df = openfile('test')
    # df.loc[len(df.index)] = ['sdfsdf']

    # print(df)
    # df = openfile('test')
    # df.loc[len(df.index)] = ['你好']
    # print(df)
    # savefile('Tom', df)
    # writefile('test', '91338master1200.jpg')
    deletefile('test', '91338master1200.jpg')
    # print(df.index['91338master1200.jpg'])
    # print(df['91338master1200.jpg'])
    # print(collection('test', '91338master1200.jpg'))
