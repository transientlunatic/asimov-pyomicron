Contributing
============

We welcome contributions to asimov-pyomicron! This guide will help you get started.

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/YOUR-USERNAME/asimov-pyomicron.git
      cd asimov-pyomicron

3. Install in development mode:

   .. code-block:: bash

      pip install -e ".[dev]"

Running Tests
-------------

Run the test suite with:

.. code-block:: bash

   python -m pytest tests/

Or run specific tests:

.. code-block:: bash

   python -m unittest tests.test_pyomicron.TestPyOmicronBasic

Code Style
----------

We follow standard Python coding conventions:

- Use PEP 8 style guide
- Maximum line length of 100 characters
- Use descriptive variable names
- Add docstrings to all public methods and classes

Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in ``docs/_build/html/``.

Submitting Changes
------------------

1. Create a new branch for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and commit them with clear commit messages
3. Push to your fork:

   .. code-block:: bash

      git push origin feature/your-feature-name

4. Open a Pull Request on GitHub

Pull Request Guidelines
------------------------

- Describe your changes clearly in the PR description
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Add tests for new features

Reporting Issues
----------------

If you find a bug or have a feature request:

1. Check if the issue already exists on GitHub
2. If not, create a new issue with:
   - Clear description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected and actual behavior
   - Your environment (OS, Python version, etc.)

Questions?
----------

If you have questions about contributing, feel free to:

- Open an issue on GitHub
- Ask in the discussions section
- Contact the maintainers

Thank you for contributing to asimov-pyomicron!
