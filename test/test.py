from base64 import urlsafe_b64decode,urlsafe_b64encode

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

if __name__ == '__main__':
    a = 'admin@123'

    b = strTransB64(a)
    print(b)
    c = b64TransString(b)
    print(c)