# 项目事件管理工具-后端接口文档
## 作者
Edmond
1. 登录接口

    ip:port/api/v1.0/auth/loginUser

接口功能描述:

    登录系统，在后台建立session，并在此基础上确认用户的权限。

请求报文负载：

    json:
        {'userid':userid,
         'username':'username',
         'passwd':'passwd'}

请求报文值说明：

| 编号 | 值       | 说明             | 非空 | 类型   |
| :--- | :------- | :--------------- | ---- | ------ |
| 1    | userid   | 用户id           | Y    | int    |
| 2    | username | 用户名           | Y    | string |
| 3    | passwd   | base64编码的密码 | Y    | string |

反馈报文负载：

    json:
        {'error_code':error code,
        'error_msg':'error message',
        'args':'error arguments'}

反馈报文值说明：

| 编号 | 值         | 说明                                               | 非空 | 类型   |
| :--- | :--------- | :------------------------------------------------- | ---- | ------ |
| 1    | error_code | 错误编码                                           | Y    | int    |
| 2    | error_msg  | 具体错误信息，如数据库错误将返回数据库详细错误报文 | Y    | string |
| 3    | args       | 出错的参数名                                       | Y    | string |

反馈报文errorcode枚举：

| 编号 | http code 值 | error code 值 | 说明                                                         |
| :--- | :----------- | :------------ | ------------------------------------------------------------ |
| 1    | 401          | 1400          | 认证不通过，缺少userid、username、passwd参数值任意一个或全部 |
| 2    | 521          | 1699          | 未确认的捕获错误，请联系管理员检查日志文件                   |
| 3    | 523          | 1700          | 数据库反馈错误，具体请见反馈报文详细内容                     |
| 4    | 200          | 2000          | 用户登录成功                                                 |