# 目录树介绍

以下为当前 Dandelion 组件主要的目录树，下面会进行逐一介绍。

```
dandelion
├── alembic.ini
├── dandelion
│   ├── alembic
│   ├── api
│   │   ├── api_v1
│   │   │   ├── api.py
│   │   │   ├── endpoints
│   │   │   └── __init__.py
│   │   ├── deps.py
│   │   └── __init__.py
│   ├── conf
│   ├── constants.py
│   ├── core
│   │   ├── __init__.py
│   │   └── security.py
│   ├── crud
│   ├── db
│   │   ├── base_class.py
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── redis_pool.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   ├── mqtt
│   ├── periodic_tasks.py
│   ├── py.typed
│   ├── schemas
│   ├── tests
│   ├── util
│   └── version.py
├── doc
├── Dockerfile
├── dprint.json
├── etc
│   └── dandelion
│       ├── dandelion.conf
│       ├── dandelion-config-generator.conf
│       ├── dandelion.conf.sample
│       └── gunicorn.py
├── LICENSE
├── mypy.ini
├── README.rst
├── README-zh_CN.rst
├── requirements.txt
├── setup.cfg
├── setup.py
├── swagger.json
├── test-requirements.txt
├── tools
│   ├── datainit.py
│   ├── generate_swagger.py
│   └── run_service.sh
└── tox.ini
```

## RESTful API 定义

- `dandelion/api/api_v1` 目录下，为当前 v1 版本的 API 定义的地方
- `dandelion/api/deps.py` 文件，为 API 中使用到的 Depends 方法
- `dandelion/schemas` 目录下，定义 API 请求及返回数据的 schema 信息

## 配置相关

- `dandelion/conf` 目录下，定义组件使用到的配置参数
- `etc/dandelion/dandelion.conf.sample` 文件，为组件生成的默认配置文件
- `etc/dandelion/dandelion-config-generator.conf` 文件，定义了生成默认配置文件的 namespace 范围，再使用
  `tox -e genconfig` 既能生成默认配置文件

## 数据库相关

- `dandelion/crud` 目录下，为针对 ORM 的 CRUD 操作
- `dandelion/db` 目录下，定义了 mariadb 的连接以及 redis 的连接
- `dandelion/models` 目录下，定义所有数据库模型 ORM ，此处有增加或者相应修改，就需要使用 alembic 产生迁移脚本

## alembic 数据库迁移相关

- `alembic.ini` 为配置文件，一般情况下，不太会需要修改此文件
- `alembic` 目录，会在执行 `alembic revision --autogenerate -m "xxxx"` 后，会在此目录的 `versions` 子目录下生成对应的迁移脚本

## 消息队列

- `dandelion/mqtt` 目录下，定义了针对 mqtt 的监听以及相关操作

## 其它

- `dandelion/util` 目录下，是一些公共方法
- `dandelion/periodic_tasks.py` 文件中，定义了一些定时任务
- `dandelion/constants.py` 文件中，定义了一些常量
- `dandelion/main.py` 文件中，定义了服务启动的一些配置
- `etc/dandelion/gunicorn.py` 文件，定义了使用 gunicorn 启动服务时的一些参数设置
- `tools/datainit.py` 文件，目前组件的一些初始化数据脚本
- `tools/generate_swagger.py` 文件，生成离线 swagger.json 文件
