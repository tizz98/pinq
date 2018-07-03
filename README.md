# pinq
A [LINQ](https://msdn.microsoft.com/en-us/library/bb308959.aspx) style API for Python iterables. Inspired by [JINQ](https://github.com/VivekRagunathan/JINQ).

## Installation
```
pip install pinq
```

## Docs
These are a work in progress. For now, check out the [unit tests](./tests).

## Tests
When contributing, make sure the test code coverage is not below 100%. To run tests:
```
pip install -e .
pytest tests --cov=pinq
flake8 pinq tests
```
