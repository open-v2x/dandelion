============================
OpenV2X 设备管理 - APIServer
============================

|pep8| |ci| |issue| |star| |license|

`English <./README.rst>`__ \| 简体中文

目录
----

-  `OpenV2X 设备管理 - APIServer <#openv2x-设备管理---apiserver>`__

   -  `目录 <#目录>`__
   -  `配置 <#配置>`__
   -  `构建 && 运行 (Linux) <#构建--运行-linux>`__
   -  `本地开发 (Linux) <#本地开发-linux>`__

      -  `运行服务 <#运行服务>`__
      -  `Alembic (数据库迁移) <#alembic-数据库迁移>`__
      -  `Tox 工具 <#tox-工具>`__

配置
----

-  **样例文件:**
   `dandelion.conf.sample <./etc/dandelion/dandelion.conf.sample>`__

-  首先，你需要从样例文件中拷贝一份配置文件。

   .. code:: bash

      cp etc/dandelion/dandelion.conf.example etc/dandelion/dandelion.conf

-  通常，你应该修改以下配置属性值：

   .. code:: yaml

      [DEFAULT]
      debug: true
      log_file: dandelion.log
      log_dir: /var/log/dandelion

      [cors]
      origins: *

      [database]
      connection: mysql+pymysql://dandelion:dandelion@127.0.0.1:3306/dandelion

      [mqtt]
      host: 127.0.0.1
      port: 1883
      username: root
      password: 123456

      [redis]
      connection: redis://root:123456@127.0.0.1:6379?db=0&socket_timeout=60&retry_on_timeout=yes

      [token]
      expire_seconds: 604800

-  最后，你可以将 ``etc/dandelion/dandelion.conf`` 链接至
   ``/etc/dandelion/dandelion.conf``\ 。

   .. code:: bash

      mkdir -p /etc/dandelion
      DANDELION_PATH=`pwd`
      cd /etc/dandelion
      ln -s ${DANDELION_PATH}/etc/dandelion/dandelion.conf dandelion.conf

构建 && 运行 (Linux)
--------------------

-  构建 docker 镜像

   .. code:: bash

      RELEASE_VERSION=`git rev-parse --short HEAD`_`date -u +%Y-%m-%dT%H:%M:%S%z`
      GIT_BRANCH=`git rev-parse --abbrev-ref HEAD`
      GIT_COMMIT=`git rev-parse --verify HEAD`
      docker build --no-cache --pull --force-rm --build-arg RELEASE_VERSION=${RELEASE_VERSION} --build-arg GIT_BRANCH=${GIT_BRANCH} --build-arg GIT_COMMIT=${GIT_COMMIT} -f Dockerfile -t dandelion:latest .

-  以容器方式运行 dandelion 服务

   .. code:: bash

      mkdir -p /var/log/dandelion
      docker run -d --name dandelion_bootstrap -e KOLLA_BOOTSTRAP="" -v /etc/dandelion/dandelion.conf:/etc/dandelion/dandelion.conf --net=host dandelion:latest
      docker rm dandelion_bootstrap
      docker run -d --name dandelion --restart=always -v /etc/dandelion/dandelion.conf:/etc/dandelion/dandelion.conf -v /var/log/dandelion:/var/log/dandelion --net=host dandelion:latest

本地开发 (Linux)
----------------

运行服务
~~~~~~~~

-  在你运行 dandelion 服务前，你需要按照 `配置 <#配置>`__ 章节操作。

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      uvicorn --reload --reload-dir dandelion --port 28300 --log-level debug dandelion.main:app --host 0.0.0.0

-  你可以在 ``http://127.0.0.1:28300/docs`` 地址访问 OpenAPI swagger 文档。

Alembic (数据库迁移)
~~~~~~~~~~~~~~~~~~~~

-  生成迁移脚本.

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      alembic revision --autogenerate -m "xxxx"

-  运行迁移脚本以及更新数据库。

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      alembic upgrade head

Tox 工具
~~~~~~~~

-  生成最新的 swagger 文件。

   .. code:: bash

      tox -e genswagger

-  生成最新的样例配置文件。

   .. code:: bash

      tox -e genconfig

-  代码格式化以及样式检查。

   .. code:: bash

      tox -e pep8-format
      tox -e pep8

.. |pep8| image:: https://github.com/open-v2x/dandelion/actions/workflows/tox-pep8.yml/badge.svg?event=push
   :target: https://github.com/open-v2x/dandelion/actions/workflows/tox-pep8.yml
.. |ci| image:: https://github.com/open-v2x/dandelion/actions/workflows/ci.yml/badge.svg?event=push
   :target: https://github.com/open-v2x/dandelion/actions/workflows/ci.yml
.. |issue| image:: https://img.shields.io/github/issues/open-v2x/dandelion
   :target: https://github.com/open-v2x/dandelion/issues
.. |star| image:: https://img.shields.io/github/stars/open-v2x/dandelion
   :target: #
.. |license| image:: https://img.shields.io/github/license/open-v2x/dandelion
   :target: LICENSE
