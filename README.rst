=====================================
OpenV2X Device Management - APIServer
=====================================

|pep8| |ci| |issue| |star| |license|

Table of contents
-----------------

-  `OpenV2X Device Management -
   APIServer <#openv2x-device-management---apiserver>`__

   -  `Table of contents <#table-of-contents>`__
   -  `Configuration <#configuration>`__
   -  `Build && Run (Linux) <#build--run-linux>`__
   -  `Local Development (Linux) <#local-development-linux>`__

      -  `Run server <#run-server>`__
      -  `Alembic (Database Migration) <#alembic-database-migration>`__
      -  `Tox Tools <#tox-tools>`__

Configuration
-------------

-  **Sample File:**
   `dandelion.conf.sample <./etc/dandelion/dandelion.conf.sample>`__

-  First of all, you need to copy the configuration file from sample.

   .. code:: bash

      cp etc/dandelion/dandelion.conf.example etc/dandelion/dandelion.conf

-  Generally, you should change the following values:

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

-  At last, you can link the ``etc/dandelion/dandelion.conf`` to the
   ``/etc/dandelion/dandelion.conf`` file.

   .. code:: bash

      mkdir -p /etc/dandelion
      DANDELION_PATH=`pwd`
      cd /etc/dandelion
      ln -s ${DANDELION_PATH}/etc/dandelion/dandelion.conf dandelion.conf

Build && Run (Linux)
--------------------

-  Build docker image.

   .. code:: bash

      RELEASE_VERSION=`git rev-parse --short HEAD`_`date -u +%Y-%m-%dT%H:%M:%S%z`
      GIT_BRANCH=`git rev-parse --abbrev-ref HEAD`
      GIT_COMMIT=`git rev-parse --verify HEAD`
      docker build --no-cache --pull --force-rm --build-arg RELEASE_VERSION=${RELEASE_VERSION} --build-arg GIT_BRANCH=${GIT_BRANCH} --build-arg GIT_COMMIT=${GIT_COMMIT} -f Dockerfile -t dandelion:latest .

-  Run dandelion service as container.

   .. code:: bash

      mkdir -p /var/log/dandelion
      docker run -d --name dandelion_bootstrap -e KOLLA_BOOTSTRAP="" -v /etc/dandelion/dandelion.conf:/etc/dandelion/dandelion.conf --net=host dandelion:latest
      docker rm dandelion_bootstrap
      docker run -d --name dandelion --restart=always -v /etc/dandelion/dandelion.conf:/etc/dandelion/dandelion.conf -v /var/log/dandelion:/var/log/dandelion --net=host dandelion:latest

Local Development (Linux)
-------------------------

Run server
~~~~~~~~~~

-  Before you run the dandelion server, you need to follow the
   `Configuration <#configuration>`__ section.

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      uvicorn --reload --reload-dir dandelion --port 28300 --log-level debug dandelion.main:app --host 0.0.0.0

-  You can visit the OpenAPI swagger document at
   ``http://127.0.0.1:28300/docs``

Alembic (Database Migration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Generate the migration script.

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      alembic revision --autogenerate -m "xxxx"

-  Run the migration script and update the database.

   .. code:: bash

      tox -e venv
      source .tox/venv/bin/activate
      alembic upgrade head

Tox Tools
~~~~~~~~~

-  Generate the latest swagger file.

   .. code:: bash

      tox -e genswagger

-  Generate the latest sample config file.

   .. code:: bash

      tox -e genconfig

-  Code format and style check.

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
