<a name="readme-top"></a>

<div align="center">
  <h2 align="center">Cryptoserve</h2>
  <p align="center">
    Server-based software for learning modern Cryptography.
    <br />
    <br />
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#documentation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About The Project

Cryptoserve is a server framework that hosts a library of cryptography-related exercises, designed to help students learn a broad range of cryptographic concepts through hands-on experimentation.

Each exercise defines a protocol in which Cryptoserve controls one side of the interaction. Students are responsible for implementing the other side of the exchange in order to complete the challenge.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

To get this project up and running, please follow the steps shown below.


### Prerequisites

This project relies on [Poetry](https://python-poetry.org/) for dependency management. You can find instructions on how to download it [here](https://python-poetry.org/docs/#installation).


### Installation

Once Poetry is installed...

1. Clone the repository.

   ```sh
   git clone https://github.com/PeanutButterRat/cryptoserve.git
   ```
2. Install the project with Poetry.

   ```sh
   cd cryptoserve  # You should now be in the project folder.
   poetry install
   ```


### Documentation

Cryptoserve relies on [Sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. If you are simply interested in *viewing* the documentation, you can find it online [here](https://cryptoserve.readthedocs.io/en/latest/).

By default, the project is not configured to install documentation-related dependencies. If you would like to build the documentation locally, you'll need to install some additional packages.

1. Reinstall the project with the `docs` group enabled.

   ```sh
   poetry install --with docs
   ```

2. Use the Makefile to build the documentation. More advanced options are available [here](https://www.sphinx-doc.org/en/master/usage/quickstart.html#).

   ```sh
   cd docs    # You should now be in cryptoserve/docs
   make html  # Build the HTML version of the documentation.
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

To run Cryptoserve, use Poetry from the command line.

   ```sh
   poetry run cryptoserve
   ```


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
