# pyark

pyark is a python client to the Clinical Variant Ark (CVA) REST API 
[https://github.com/genomicsengland/clinical_variant_ark](https://github.com/genomicsengland/clinical_variant_ark).
pyark primary aim is to facilitate access to CVA knowledge base hiding the complexity using the REST API. 
Also by integrating with major Python data analysis libraries it aims at enabling an analytical framework on CVA.

## Getting Started

### Prerequisites

pyark works with python 2.7 up to python 3.6.

### Installing

Install with pip:

```
pip install clinical-variant-ark
```

You will need a CVA server up and running and you will need credentials with the right authorisation permissions.

Initialise the client:
```python
from pyark.cva_client import CvaClient

cva = CvaClient(url_base="https://your.cva", user="you", password="your_secret")
cases_client = cva.cases()
pedigrees_client = cva.pedigrees()
entities_client = cva.entities()
variants_client = cva.variants()
report_events_client = cva.report_events()
transactions_client = cva.transactions()
```

Query CVA's knowledge base:
```python
cases_client.count()
```

Check the version of the client you are using:
```python
import pyark

print("pyark version {}".format(pyark.VERSION))
```

See the documentation for further usage at [https://genomicsengland.github.io/pyark/](https://genomicsengland.github.io/pyark/).

## Running the tests

Set the following environment variables:
```bash
export CVA_URL_BASE="https://your.cva"
export CVA_USER="you"
export CVA_PASSWORD="your_secret"
```

Then run unit tests:
```bash
python -m unittest discover
```

These tests rely on a working CVA server with some data in it.

## Versioning

We use [semantic versioning](http://semver.org/). The major and minor versions are aligned with the CVA backend versioning. 

## Authors

* **Pablo Riesgo Ferreiro** [priesgo](https://github.com/priesgo)
* **Kevin Savage** [kevinpetersavage](https://github.com/kevinpetersavage)
* **William Bellamy** [squinker](https://github.com/squinker)

See also the list of [contributors](https://github.com/genomicsengland/pyark/contributors) who participated in this project.

## License

This project is licensed under the Apache v2.0 license - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Genomics England bioinformatics team as an infinite source of requirements
* Katherine Smith and Augusto Rendon for spending their time playing with pyark!
* Antonio Rueda Martin for listening to us
