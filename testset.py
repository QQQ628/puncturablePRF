
import random

y = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def text_create(name):
        desktop_path = "C:\\Users\\ryk\\Desktop\\"  # 新创建的txt文件的存放路径，路径可修改哦
        full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        # file.write(msg)  # msg也就是下面的Hello world!
        file.close()

def ran():
    num = random.randint(0, 51)
    return num

def data_generate(n):
    file = open("C:\\Users\\ryk\\Desktop\\textfile.txt", 'a')

    a = 0
    b = int(n)
    while a < b:
        line = str(a) + " " + y[ran()] +";"
        file.write(line)
        a += 1
    file.close()  # msg也就是下面的Hello world!

if  __name__ == '__main__':
    n = input("请输入测试集的数量：")
    text_create('textfile')
    data_generate(n)
