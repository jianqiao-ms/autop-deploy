# API Project

## Dependencies
```bash
$ sudo pip3 install django mysqlclient paramiko channels
```

## Frequently used django-admin cmd

* 创建项目
    ```text
    $ django-admin startproject api 
    ``` 
## Frequently used manage.py cmd
* 创建应用
    ```text
    $ python3 manage.py startapp api
    ```
* 创建管理员账号
    ```text
    $ python3 manage.py createsuperuser
    ```
* 运行开发环境
    ```text
    $ python3 manage.py runserver 0:8000
    ```
### Database
* 创建表
    ```text
    $ python3 manage.py migrate
    ```

# Troubleshooting  
## Error code
| Error code | Description |
| --- | --- |
| 1xx | Error during start |
| 101 | 读取配置文件(json)并序列化为python字典对象失败 |
| 102 | Upload path permmision problem |
| 103 | Cannot connect to gitlab |

