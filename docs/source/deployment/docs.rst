.. _documentation_hosting:

Hosting the Documentation
=========================

This section describes how to build and serve the Cryptoserve documentation locally or within a Docker container. The documentation is built using **Sphinx** and follows standard reStructuredText practices.

Prerequisites
-------------

To build the documentation, you will need the same core tools listed in :ref:`server_hosting`:


Building the Documentation Locally
-------------------------

1. **Clone the Repository** (if not already done):

   .. code-block:: bash

      git clone https://github.com/PeanutButterRat/cryptoserve.git
      cd cryptoserve

2. **Install Dependencies with Poetry**

   .. code-block:: bash

      poetry install --with docs

3. **Build the HTML Documentation**

   Navigate to the `docs/` directory and build the docs:

   .. code-block:: bash

      cd docs
      poetry run make html

   The generated site will be available in `_build/html/index.html`. You can open it in any web browser.


Docker Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cryptoserve's Dockerfile also supports building the documentation in a containerized environment.

1. **Build the Docker Image**

   .. code-block:: bash

      docker build --target docs-runtime -t cryptoserve-docs .

2. **Run the Container to Build Docs**

   .. code-block:: bash

      docker run -p 8080:80 cryptoserve-docs

.. note::

   In the future, pre-built Docker images may be hosted on GitHub Container Registry for easier deployment.
   Instructions for using those images will be added when that feature is available.
