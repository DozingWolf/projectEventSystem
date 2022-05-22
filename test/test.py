from sys import exc_info
from base64 import urlsafe_b64decode,urlsafe_b64encode
from tool.sqlGenerator import updateSqlGenerator

def b64TransString(input:str):
    # 将base64转换为password
    b64bytes = bytes(input,encoding='utf8')
    # current_app.logger.debug('password is : %s'%b64bytes)
    passwd = urlsafe_b64decode(b64bytes).decode('utf-8')
    print('str password is : %s'%passwd)
    return passwd

def strTransB64(input:str):
    # 将字符串转换为base64
    bytesStr = bytes(input,encoding='utf8')
    encryptStr = urlsafe_b64encode(bytesStr).decode('utf-8')
    print('encrypt string is %s'%encryptStr)
    return encryptStr

def test1():
    a = 'admin@123'
    b = strTransB64(a)
    print(b)
    c = b64TransString(b)
    print(c)

def update():
    data = {'set':{
                    'projectcode':'PRJ001',
                    'projectname':'project_name_samlpe'
                },
            'where':{
                    'id':{
                            'operation':'equl',
                            'data':1
                            },
                    'createuser':{
                            'operation':'bulabula',
                            'data':'csy'
                            }
                    }
            }
    setchecklist = ['projectcode','projectname']
    wherechecklist = ['id','createuser']
    try:
        updateSqlGenerator(querypara=data,setchecklist=setchecklist,querychecklist=wherechecklist,tname='table_name')
    except Exception as err:
        print(err)
        print(exc_info())

if __name__ == '__main__':
    update()