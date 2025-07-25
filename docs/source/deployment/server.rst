.. _server_hosting:

Server Deployment
================

This guide explains how to deploy the Cryptoserve server for local development, classroom exercises, or remote access.


Requirements
------------

To run Cryptoserve, you will need:

- `Python 3.11+ <https://www.python.org/downloads/>`_
- `Poetry <https://python-poetry.org/>`_
- Optionally, `Docker <https://docs.docker.com/desktop/>`_ (for containerized deployment)


Local Setup (Poetry)
--------------------

1. **Install Poetry**

   Follow the official installation to install Poetry `here <ttps://python-poetry.org/docs/#installation>`_.

2. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/PeanutButterRat/cryptoserve.git
      cd cryptoserve

3. **Install Dependencies**

   .. code-block:: bash

      poetry install

4. **Run the Server**

   .. code-block:: bash

      poetry run cryptoserve

   You can now interact with the server at `localhost:5050`.


Docker Deployment
-----------------

Cryptoserve also supports containerized deployment using Docker. To build and run the server in a Docker container:

1. **Build the Docker Image**

   .. code-block:: bash

      docker build --target app-runtime -t cryptoserve .

2. **Run the Docker Container**

   .. code-block:: bash

      docker run -p 5050:5050 cryptoserve

.. note::

   In the future, pre-built Docker images may be hosted on GitHub Container Registry for easier deployment.
   Instructions for using those images will be added when that feature is available.
