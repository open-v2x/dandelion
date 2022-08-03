# 如何开发

## 想要提供新的 RESTful API

1. 在目录 `dandelion/api/api_v1/endpoints` 目录下新建文件，可以以对象名称命名文件；
2. 然后在文件中，实现 API 的 增删改查，可以参考其它文件；
3. 重要的一点，最后，要在 `dandelion/api/api_v1/api.py` 文件中，注册路由；

## 想要新增数据库模型

1. 在目录 `dandelion/models` 目录下新建文件，可以以对象名称命名文件；
2. 然后在文件中，定义模型的字段以及属性等，可以参考其它文件；
3. 当然，我们可以在 `__init__.py` 中先引入此模块，后续直接 `from dandelion import models` 及 `models.XXX` 即可调用；
4. 定义完成后，需要执行 `tox -e venv`, `source .tox/venv/bin/activate` 以及
   `alembic revision --autogenerate -m "xxxx"` 生成迁移脚本，脚本最终位于 `dandelion/alembic/versions` 目录下；

## 想要操作 redis

1. 首先引入 `from dandelion.api.deps import get_redis_conn`
2. 然后 `redis_conn = get_redis_conn()`

## 想要新增定时任务

1. 可以在 `dandelion/periodic_tasks.py` 中新增方法；
2. 参考 `dandelion/main.py` 中的 `setup_rsu_running` 写法；

## 其它

- 开发后，本地调试：

1. tox -e venv
2. source .tox/venv/bin/activate
3. uvicorn --reload --reload-dir dandelion --port 28300 --log-level debug dandelion.main:app --host
   0.0.0.0
4. 打开浏览器，访问 `http://a.b.c.y:28300/docs` 即可开始验证功能；

- 在最终提交代码前，必须要做的事情：

1. tox -e pep8-format 执行代码格式化
2. tox -e pep8 执行代码风格的再次检查
3. tox -e genconfig 生成 sample 配置文件
4. tox -e genswagger 生成 swagger.json 离线文件
