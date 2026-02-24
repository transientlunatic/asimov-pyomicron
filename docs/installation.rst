Installation
============

Requirements
------------

- Python >= 3.9
- asimov >= 0.5
- pyomicron >= 3.0
- liquid >= 4.0

Install from PyPI
-----------------

The recommended way to install asimov-pyomicron is using pip:

.. code-block:: bash

   pip install asimov-pyomicron

Install from source
-------------------

You can also install from the source repository:

.. code-block:: bash

   git clone https://github.com/transientlunatic/asimov-pyomicron.git
   cd asimov-pyomicron
   pip install .

Development installation
-------------------------

For development, install in editable mode with development dependencies:

.. code-block:: bash

   git clone https://github.com/transientlunatic/asimov-pyomicron.git
   cd asimov-pyomicron
   pip install -e ".[dev]"

This will install the package in editable mode along with tools for testing and documentation.

Verifying installation
-----------------------

You can verify that the package is installed correctly by checking that the pipeline is registered with asimov:

.. code-block:: python

   from asimov.pipeline import known_pipelines
   print('pyomicron' in known_pipelines())

Or by importing the pipeline class directly:

.. code-block:: python

   from asimov_pyomicron import PyOmicron
   print(PyOmicron.name)  # Should print: pyomicron
