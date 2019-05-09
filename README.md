# Install gel report models dep

pip install gelreportmodels==7.2.6 --index-url=https://pypi.gel.zone/genomics/dev

# The CVA Python client: pyark

Pyark is a python client to the Clinical Variant Ark (CVA) REST API [https://github.com/genomicsengland/clinical_variant_ark](https://github.com/genomicsengland/clinical_variant_ark). This documentation is intended as a guide to the REST API too, every call to the client builds a number of REST calls to the backend behind the scenes and those URLs are shown below.

This guide does not intend to cover the whole API but just three particular use cases: having a shallow overview of the content in the database, select a  case following certain criteria and explore all the available data about a given case. More complex analysis can be done using pyark, but these are not shown here.

## Makes all necessary imports and initialise the Python CVA client

NOTE: it is handy to set the log level to INFO in order to see the times that each query takes and see how the URL is built.

The client gets a token and renews it if necessary behind the scenes.


```python
from pyark.cva_client import CvaClient
from protocols.reports_5_0_0 import Program, Tier
from protocols.cva_1_0_0 import ReportEventType
from collections import defaultdict, OrderedDict
import getpass
import logging
import pandas as pd
```


```python
# sets logging messages so the URLs that are called get printed
logging.basicConfig(level=logging.INFO)

# initialise CVA client and subclients
user = getpass.getpass("Username: ")
password = getpass.getpass("Password: ")
url = "http://localhost:8080"
cva = CvaClient(url_base=url, user=user, password=password)
cases_client = cva.cases()
pedigrees_client = cva.pedigrees()
panels_client = cva.panels()
variants_client = cva.variants()
report_events_client = cva.report_events()
transactions_client = cva.transactions()

```

    Username: ········
    Password: ········


    INFO:root:2018-08-05 09:43:46.711710 POST http://localhost:8080/cva/api/0/authentication? Accept=application/json
    INFO:root:Response time : 305 ms


## Count number of elements in the database

The main elements in CVA are:
* Report Events
* Cases
* Variants


```python
# count the total number of report events
report_events_client.count_report_events()
```

    INFO:root:2018-08-05 09:43:47.144482 GET http://localhost:8080/cva/api/0/report-events?count=True Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=277, Date=Sun, 05 Aug 2018 08:43:47 GMT
    INFO:root:Response time : 65 ms





    191371




```python
# count the number of report events with a certain criteria
report_events_client.count_report_events(
    params={'program':Program.rare_disease, 'panel_name':"cakut", 'families':['1', '2']})
```

    INFO:root:2018-08-05 09:43:47.203411 GET http://localhost:8080/cva/api/0/report-events?count=True&panel_name=cakut&program=rare_disease&families=1&families=2 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=272, Date=Sun, 05 Aug 2018 08:43:47 GMT
    INFO:root:Response time : 23 ms





    0




```python
cases_client.count_cases()
```

    INFO:root:2018-08-05 09:43:47.251949 GET http://localhost:8080/cva/api/0/cases?count=True Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=275, Date=Sun, 05 Aug 2018 08:43:47 GMT
    INFO:root:Response time : 21 ms





    1410




```python
# NOTE: this count is wrong because the test database needs reloading with the latest version
cases_client.count_cases(params={'program':Program.rare_disease, 'panel_name':"intellectual disability"})
```

    INFO:root:2018-08-05 09:43:47.303665 GET http://localhost:8080/cva/api/0/cases?count=True&panel_name=intellectual disability&program=rare_disease Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=274, Date=Sun, 05 Aug 2018 08:43:47 GMT
    INFO:root:Response time : 22 ms





    107




```python
variants_client.count_variants()
```

    INFO:root:2018-08-05 09:43:47.361899 GET http://localhost:8080/cva/api/0/variants?count=True Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=276, Date=Sun, 05 Aug 2018 08:43:47 GMT
    INFO:root:Response time : 22 ms





    70261



## Iterate through elements using pagination

The default page size is 200, but it can be configured using the `limit` parameter.
Pagination happens automatically using pyark, but if making raw REST queries the required coordinates for the next page are in the header of the response in the fields:
* `X-Pagination-Limit`
* `X-Pagination-Marker`

To fetch the next page, these attributes must be passed in the query parameter `limit` and `marker` respectively.




```python
# create an iterator for the report events
report_events = report_events_client.get_report_events(
    params={'program':Program.rare_disease, 'only_latest':True, 'limit':3})

# iterate through the first 5
i = 0
for report_event in report_events:
    i+=1
    if i == 5:
        break
```

    INFO:root:2018-08-05 09:43:48.384738 GET http://localhost:8080/cva/api/0/report-events?program=rare_disease&limit=3&only_latest=True Server=Apache-Coyote/1.1, Link=<?limit=3&marker=00029463-0b5c-4d88-980d-d40fd17d2f0c>; rel="next", X-Pagination-Limit=3, X-Pagination-Marker=00029463-0b5c-4d88-980d-d40fd17d2f0c, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=6052, Date=Sun, 05 Aug 2018 08:43:48 GMT
    INFO:root:Response time : 991 ms
    INFO:root:2018-08-05 09:43:49.649474 GET http://localhost:8080/cva/api/0/report-events?marker=00029463-0b5c-4d88-980d-d40fd17d2f0c&program=rare_disease&limit=3&only_latest=True Server=Apache-Coyote/1.1, Link=<?limit=3&marker=0003a920-d99a-418a-9667-477b1cf4e974>; rel="next", X-Pagination-Limit=3, X-Pagination-Marker=0003a920-d99a-418a-9667-477b1cf4e974, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=6104, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 1254 ms



```python
# create an iterator for the cases
cases = cases_client.get_cases(params={'program':Program.rare_disease, 'limit':3})

# iterate through the first 5
i = 0
for case in cases:
    i+=1
    if i == 5:
        break
```

    INFO:root:2018-08-05 09:43:49.830657 GET http://localhost:8080/cva/api/0/cases?program=rare_disease&limit=3 Server=Apache-Coyote/1.1, Link=<?limit=3&marker=00493124-4895-4c96-b7ce-1bba4c0a50bb>; rel="next", X-Pagination-Limit=3, X-Pagination-Marker=00493124-4895-4c96-b7ce-1bba4c0a50bb, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 119 ms
    INFO:root:2018-08-05 09:43:49.905947 GET http://localhost:8080/cva/api/0/cases?marker=00493124-4895-4c96-b7ce-1bba4c0a50bb&program=rare_disease&limit=3 Server=Apache-Coyote/1.1, Link=<?limit=3&marker=009cf630-c17b-482b-b363-47179eb3e845>; rel="next", X-Pagination-Limit=3, X-Pagination-Marker=009cf630-c17b-482b-b363-47179eb3e845, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 63 ms


## Summary of cases

The case is the main entity in CVA to summarise data. It is possible to create summaries filtering by certain criteria.


```python
cases_client.get_summary({'program':Program.rare_disease}, as_data_frame=True)
```

    INFO:root:2018-08-05 09:43:49.981997 GET http://localhost:8080/cva/api/0/cases/summary?program=rare_disease Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=1547, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 51 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_participants</th>
      <th>avg_questionnaire_benign</th>
      <th>avg_questionnaire_likely_benign</th>
      <th>avg_questionnaire_likely_pathogenic</th>
      <th>avg_questionnaire_na</th>
      <th>avg_questionnaire_pathogenic</th>
      <th>avg_questionnaire_vus</th>
      <th>avg_reported</th>
      <th>avg_reported_tier1</th>
      <th>avg_reported_tier2</th>
      <th>...</th>
      <th>count_questionnaire_vus</th>
      <th>count_reported</th>
      <th>count_reported_tier1</th>
      <th>count_reported_tier2</th>
      <th>count_reported_tier3</th>
      <th>count_reported_untiered</th>
      <th>count_samples</th>
      <th>count_tier1</th>
      <th>count_tier2</th>
      <th>count_tier3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.060222</td>
      <td>0.0</td>
      <td>0.006339</td>
      <td>0.07607</td>
      <td>0.019017</td>
      <td>0.160063</td>
      <td>0.082409</td>
      <td>0.413629</td>
      <td>0.131537</td>
      <td>0.155309</td>
      <td>...</td>
      <td>52</td>
      <td>261</td>
      <td>83</td>
      <td>98</td>
      <td>81</td>
      <td>40</td>
      <td>1299</td>
      <td>116</td>
      <td>420</td>
      <td>117779</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 40 columns</p>
</div>




```python
cases_summary_family1 = cases_client.get_summary({'program':Program.rare_disease, 'num_samples':1}, as_data_frame=True)
cases_summary_family2 = cases_client.get_summary({'program':Program.rare_disease, 'num_samples':2}, as_data_frame=True)
cases_summary_family3 = cases_client.get_summary({'program':Program.rare_disease, 'num_samples':3}, as_data_frame=True)
pd.concat([cases_summary_family1, cases_summary_family2, cases_summary_family3]).transpose()

```

    INFO:root:2018-08-05 09:43:50.088764 GET http://localhost:8080/cva/api/0/cases/summary?program=rare_disease&num_samples=1 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=1508, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 44 ms
    INFO:root:2018-08-05 09:43:50.134716 GET http://localhost:8080/cva/api/0/cases/summary?program=rare_disease&num_samples=2 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=1496, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 34 ms
    INFO:root:2018-08-05 09:43:50.192346 GET http://localhost:8080/cva/api/0/cases/summary?program=rare_disease&num_samples=3 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=1384, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 37 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>0</th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>avg_participants</th>
      <td>1.000000</td>
      <td>2.012048</td>
      <td>3.000000</td>
    </tr>
    <tr>
      <th>avg_questionnaire_benign</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>avg_questionnaire_likely_benign</th>
      <td>0.011111</td>
      <td>0.000000</td>
      <td>0.003906</td>
    </tr>
    <tr>
      <th>avg_questionnaire_likely_pathogenic</th>
      <td>0.029630</td>
      <td>0.096386</td>
      <td>0.109375</td>
    </tr>
    <tr>
      <th>avg_questionnaire_na</th>
      <td>0.003704</td>
      <td>0.084337</td>
      <td>0.015625</td>
    </tr>
    <tr>
      <th>avg_questionnaire_pathogenic</th>
      <td>0.096296</td>
      <td>0.144578</td>
      <td>0.230469</td>
    </tr>
    <tr>
      <th>avg_questionnaire_vus</th>
      <td>0.114815</td>
      <td>0.108434</td>
      <td>0.042969</td>
    </tr>
    <tr>
      <th>avg_reported</th>
      <td>0.277778</td>
      <td>0.506024</td>
      <td>0.519531</td>
    </tr>
    <tr>
      <th>avg_reported_tier1</th>
      <td>0.059259</td>
      <td>0.120482</td>
      <td>0.210938</td>
    </tr>
    <tr>
      <th>avg_reported_tier2</th>
      <td>0.148148</td>
      <td>0.240964</td>
      <td>0.136719</td>
    </tr>
    <tr>
      <th>avg_reported_tier3</th>
      <td>0.092593</td>
      <td>0.156627</td>
      <td>0.156250</td>
    </tr>
    <tr>
      <th>avg_reported_untiered</th>
      <td>0.022222</td>
      <td>0.084337</td>
      <td>0.093750</td>
    </tr>
    <tr>
      <th>avg_samples</th>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
    </tr>
    <tr>
      <th>avg_tier1</th>
      <td>0.092593</td>
      <td>0.204819</td>
      <td>0.261719</td>
    </tr>
    <tr>
      <th>avg_tier2</th>
      <td>0.681481</td>
      <td>1.108434</td>
      <td>0.492188</td>
    </tr>
    <tr>
      <th>avg_tier3</th>
      <td>357.514815</td>
      <td>156.746988</td>
      <td>29.898438</td>
    </tr>
    <tr>
      <th>count_cases</th>
      <td>270.000000</td>
      <td>83.000000</td>
      <td>256.000000</td>
    </tr>
    <tr>
      <th>count_cases_clinical_reports</th>
      <td>241.000000</td>
      <td>65.000000</td>
      <td>221.000000</td>
    </tr>
    <tr>
      <th>count_cases_exit_questionnaires</th>
      <td>222.000000</td>
      <td>56.000000</td>
      <td>166.000000</td>
    </tr>
    <tr>
      <th>count_cohorts</th>
      <td>269.000000</td>
      <td>83.000000</td>
      <td>256.000000</td>
    </tr>
    <tr>
      <th>count_groups</th>
      <td>269.000000</td>
      <td>83.000000</td>
      <td>256.000000</td>
    </tr>
    <tr>
      <th>count_panels</th>
      <td>41.000000</td>
      <td>33.000000</td>
      <td>35.000000</td>
    </tr>
    <tr>
      <th>count_panels_versioned</th>
      <td>54.000000</td>
      <td>37.000000</td>
      <td>45.000000</td>
    </tr>
    <tr>
      <th>count_participants</th>
      <td>270.000000</td>
      <td>167.000000</td>
      <td>768.000000</td>
    </tr>
    <tr>
      <th>count_positive_dx</th>
      <td>50.000000</td>
      <td>27.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_benign</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_likely_benign</th>
      <td>3.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_likely_pathogenic</th>
      <td>8.000000</td>
      <td>8.000000</td>
      <td>28.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_na</th>
      <td>1.000000</td>
      <td>7.000000</td>
      <td>4.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_pathogenic</th>
      <td>26.000000</td>
      <td>12.000000</td>
      <td>59.000000</td>
    </tr>
    <tr>
      <th>count_questionnaire_vus</th>
      <td>31.000000</td>
      <td>9.000000</td>
      <td>11.000000</td>
    </tr>
    <tr>
      <th>count_reported</th>
      <td>75.000000</td>
      <td>42.000000</td>
      <td>133.000000</td>
    </tr>
    <tr>
      <th>count_reported_tier1</th>
      <td>16.000000</td>
      <td>10.000000</td>
      <td>54.000000</td>
    </tr>
    <tr>
      <th>count_reported_tier2</th>
      <td>40.000000</td>
      <td>20.000000</td>
      <td>35.000000</td>
    </tr>
    <tr>
      <th>count_reported_tier3</th>
      <td>25.000000</td>
      <td>13.000000</td>
      <td>40.000000</td>
    </tr>
    <tr>
      <th>count_reported_untiered</th>
      <td>6.000000</td>
      <td>7.000000</td>
      <td>24.000000</td>
    </tr>
    <tr>
      <th>count_samples</th>
      <td>270.000000</td>
      <td>166.000000</td>
      <td>768.000000</td>
    </tr>
    <tr>
      <th>count_tier1</th>
      <td>25.000000</td>
      <td>17.000000</td>
      <td>67.000000</td>
    </tr>
    <tr>
      <th>count_tier2</th>
      <td>184.000000</td>
      <td>92.000000</td>
      <td>126.000000</td>
    </tr>
    <tr>
      <th>count_tier3</th>
      <td>96529.000000</td>
      <td>13010.000000</td>
      <td>7654.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Secondary entities

There are secondary entities that are usually used to filter the main entities. Some of these are:
* **Panel of genes**. A gene panel is a list of genes that is of specific interest for a given condition. Although each family may be analysed against multiple panels, our family analysis are panel-centric.
* **Genes**. The mapping between Ensembl identifiers and HGNC gene symbols (TODO)
* **Phenotypes**. The HPO terms including identifier, name and synonyms (TODO)


```python
# fetch the list of panel names
all_panels = panels_client.get_all_panels()
all_panels[0:5]
```

    INFO:root:2018-08-05 09:43:50.274138 GET http://localhost:8080/cva/api/0/panels/summary?use_versions=False Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=4343, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 28 ms





    [None,
     u'posterior segment abnormalities',
     u'multiple bowel polyps',
     u'intellectual disability',
     u'familial colon cancer']




```python
# fetch the list of panel names and versions and the number of cases
panels_client.get_panels_summary()[0:5]
```

    INFO:root:2018-08-05 09:43:50.323164 GET http://localhost:8080/cva/api/0/panels/summary?use_versions=True Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=6896, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 30 ms





    [{u'count_cases': 505, u'panel': {}},
     {u'count_cases': 118,
      u'panel': {u'name': u'posterior segment abnormalities', u'version': u'1.8'}},
     {u'count_cases': 88,
      u'panel': {u'name': u'intellectual disability', u'version': u'1.2'}},
     {u'count_cases': 83,
      u'panel': {u'name': u'multiple bowel polyps', u'version': u'1.6'}},
     {u'count_cases': 59,
      u'panel': {u'name': u'posterior segment abnormalities', u'version': u'1.7'}}]



## Select cases

We may want to select a set cases by different criteria


```python
# Get all cases in panel intellectual disability having 3 samples in the family
cases = cases_client.get_cases({'program':Program.rare_disease, 
                        'panel_name':'intellectual disability',
                        'num_samples':3})
print "Found {} cases".format(len(list(cases)))
```

    INFO:root:2018-08-05 09:43:50.645354 GET http://localhost:8080/cva/api/0/cases?panel_name=intellectual disability&program=rare_disease&num_samples=3 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=fb3fe05c-ef6d-4eb7-a49e-7002b658720d>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=fb3fe05c-ef6d-4eb7-a49e-7002b658720d, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:49 GMT
    INFO:root:Response time : 273 ms
    INFO:root:2018-08-05 09:43:50.718379 GET http://localhost:8080/cva/api/0/cases?marker=fb3fe05c-ef6d-4eb7-a49e-7002b658720d&panel_name=intellectual disability&program=rare_disease&limit=200&num_samples=3 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=326, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 36 ms


    Found 79 cases



```python
# Get all cases having a given gene reported
cases = cases_client.get_cases({'reported_ensembl_ids':'ENSG00000182872'})
print "Found {} cases".format(len(list(cases)))
```

    INFO:root:2018-08-05 09:43:50.786644 GET http://localhost:8080/cva/api/0/cases?reported_ensembl_ids=ENSG00000182872 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=4e144f72-81e4-4a37-9f99-18043289b9ff>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=4e144f72-81e4-4a37-9f99-18043289b9ff, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=7541, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 48 ms
    INFO:root:2018-08-05 09:43:50.852816 GET http://localhost:8080/cva/api/0/cases?marker=4e144f72-81e4-4a37-9f99-18043289b9ff&reported_ensembl_ids=ENSG00000182872&limit=200 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=326, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 55 ms


    Found 1 cases



```python
# Get all cases having any phenotype from a list
cases = cases_client.get_cases({'proband_hpo_terms':['HP:0002616', 'HP:0003124']})
print "Found {} cases".format(len(list(cases)))
```

    INFO:root:2018-08-05 09:43:50.930804 GET http://localhost:8080/cva/api/0/cases?proband_hpo_terms=HP:0002616&proband_hpo_terms=HP:0003124 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=ec169224-2a6e-44bc-85c7-0ec9ef58c9b9>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=ec169224-2a6e-44bc-85c7-0ec9ef58c9b9, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 56 ms
    INFO:root:2018-08-05 09:43:50.988773 GET http://localhost:8080/cva/api/0/cases?marker=ec169224-2a6e-44bc-85c7-0ec9ef58c9b9&limit=200&proband_hpo_terms=HP:0002616&proband_hpo_terms=HP:0003124 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=326, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 51 ms


    Found 4 cases



```python
# Get all cases having all phenotypes from a list
cases = cases_client.get_cases({'proband_hpo_terms':['HP:0002616', 'HP:0003124'],
                               'any_or_all_hpos':'ALL'})
print "Found {} cases".format(len(list(cases)))
```

    INFO:root:2018-08-05 09:43:51.071841 GET http://localhost:8080/cva/api/0/cases?any_or_all_hpos=ALL&proband_hpo_terms=HP:0002616&proband_hpo_terms=HP:0003124 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=39844384-c830-4896-a1f9-e6088d002fb9>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=39844384-c830-4896-a1f9-e6088d002fb9, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 56 ms
    INFO:root:2018-08-05 09:43:51.144047 GET http://localhost:8080/cva/api/0/cases?any_or_all_hpos=ALL&marker=39844384-c830-4896-a1f9-e6088d002fb9&limit=200&proband_hpo_terms=HP:0002616&proband_hpo_terms=HP:0003124 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=326, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 63 ms


    Found 1 cases


## Get all data about a given case

The information about any given case is distributed across: the cases, the report events, the variants and the pedigree.
Given that we have the case id and version we will be able to fetch all data relative to that case.

* **Cases**. Contain the basic information about a given case, including lists of relevant variants and case status (open/closed, solved/unsolved).
* **Report events**. Contain the full information about the segregation of a variant within a family and why this was selected in each condition. The same variant may have multiple report events, because it was selected in multiple steps of the interpretation or because it was relevant in more than one panel (ie: the same case may be analysed against multiple panels)
* **Variants**. Contain the coordinates of any given variant in two assemblies GRCh37 and GRCh38 and the Cellbase annotations in those.
* **Pedigree**. Contain the detailed information about a family and its members. Each case will have only one pedigree.


```python
# get a case
case = cases_client.get_case(identifier="132", version=1, as_data_frame=True)
print "There are {} attributes for a case".format(case.size)
```

    INFO:root:2018-08-05 09:43:51.186688 GET http://localhost:8080/cva/api/0/cases/132/1? Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 21 ms


    There are 143 attributes for a case



```python
# get a pedigree for a case
ped = pedigrees_client.get_pedigree(identifier="132", version=1, as_data_frame=True)
len(ped.keys())
```

    INFO:root:2018-08-05 09:43:51.249852 GET http://localhost:8080/cva/api/0/pedigrees/132/1? Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 24 ms





    11




```python
# get the details about the members of a pedigree
members = []
for member in ped['pedigree.members'][0]:
    members.append(pd.DataFrame(member.items(), columns=['attribute', member['participantId']]))
reduce(lambda x, y: pd.merge(x, y, on = 'attribute'), members).shape
```




    (25, 4)




```python
# get all report events for a case
report_events = report_events_client.get_report_events(params={'case_id':"132", 'case_version':1})
print "Found {} report events for the case".format(len(list(report_events)))
```

    INFO:root:2018-08-05 09:43:51.401257 GET http://localhost:8080/cva/api/0/report-events?case_id=132&case_version=1 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=f9565433-fedd-401e-b432-703af6a662ad>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=f9565433-fedd-401e-b432-703af6a662ad, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 79 ms
    INFO:root:2018-08-05 09:43:51.479339 GET http://localhost:8080/cva/api/0/report-events?marker=f9565433-fedd-401e-b432-703af6a662ad&case_id=132&limit=200&case_version=1 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=243, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 38 ms


    Found 41 report events for the case



```python
# get all report events in a case for a given variant
case = cases_client.get_case(identifier="132", version=1, as_data_frame=False)
variant = case['tieredVariants'][Tier.TIER3][0]
report_events = report_events_client.get_report_events(params={'case_id':"132", 'case_version':1, 'variants':[variant]})
print "Found {} report events for the given variant in the case".format(len(list(report_events)))
```

    INFO:root:2018-08-05 09:43:51.527163 GET http://localhost:8080/cva/api/0/cases/132/1? Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 22 ms
    INFO:root:2018-08-05 09:43:51.589534 GET http://localhost:8080/cva/api/0/report-events?variants=GRCh38: 2: 178718448:T:C&case_id=132&case_version=1 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=d6fdd144-bebb-4c43-a5c4-dc75d79e2ccb>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=d6fdd144-bebb-4c43-a5c4-dc75d79e2ccb, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=3400, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 46 ms
    INFO:root:2018-08-05 09:43:51.639574 GET http://localhost:8080/cva/api/0/report-events?marker=d6fdd144-bebb-4c43-a5c4-dc75d79e2ccb&variants=GRCh38: 2: 178718448:T:C&case_id=132&limit=200&case_version=1 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=243, Date=Sun, 05 Aug 2018 08:43:50 GMT
    INFO:root:Response time : 42 ms


    Found 1 report events for the given variant in the case



```python
# fetch the report events together with all Cellbase annotations using `full_populate=true`
report_events = report_events_client.get_report_events(
    params={'case_id':"132", 'case_version':1, 'full_populate':True})
variant_annotations = report_events.next().observedVariants[0].variant
biotypes = [ct.biotype for ct in variant_annotations.variants[0].variant.annotation.consequenceTypes]
print "The variant in the first report event is annotated with biotypes: {}".format(", ".join(biotypes))
```

    INFO:root:2018-08-05 09:43:52.980764 GET http://localhost:8080/cva/api/0/report-events?full_populate=True&case_id=132&case_version=1 Server=Apache-Coyote/1.1, Link=<?limit=200&marker=f9565433-fedd-401e-b432-703af6a662ad>; rel="next", X-Pagination-Limit=200, X-Pagination-Marker=f9565433-fedd-401e-b432-703af6a662ad, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:52 GMT
    INFO:root:Response time : 1146 ms


    The variant in the first report event is annotated with biotypes: retained_intron, protein_coding, protein_coding, protein_coding, protein_coding, protein_coding, nonsense_mediated_decay, protein_coding, protein_coding, protein_coding, protein_coding, retained_intron, retained_intron, protein_coding, retained_intron, retained_intron, retained_intron, protein_coding, retained_intron, protein_coding, protein_coding, retained_intron, 


## Get similar cases

At the moment we have implemented two endpoints returning similar cases:
* Phenotypic similarity based on the HPO ontology and the annotations of terms to diseases
* Genotypic similarity based on similar variants found
    - Exact same variant
    - Same gene (TODO)
    - Other similar variants or genes (TODO)

NOTE: changes to come on case similarity metrics...



```python
# get top 10 similar cases to case 1000-1 prioritised by score
similar_cases = cases_client.get_similar_cases_by_case("132", 1, similarity_metric='PHENODIGM', limit=10)
print "Found {} cases with score {}".format(len(similar_cases), ", ".join([str(c['score']) for c in similar_cases]))
```

    INFO:root:2018-08-05 09:43:54.565130 GET http://localhost:8080/cva/api/0/cases/132/1/similar-cases?limit=10&similarity_metric=PHENODIGM Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=817, Date=Sun, 05 Aug 2018 08:43:54 GMT
    INFO:root:Response time : 530 ms


    Found 10 cases with score 1.0, 0.1423025, 0.13333334, 0.1254363, 0.12385842, 0.11517511, 0.08257228, 0.05, 0.05, 0.05



```python
# get top 10 similar cases to the list of phenotypes HP:0002616, HP:00012345 prioritised by score
similar_cases = cases_client.get_similar_cases_by_phenotypes(['HP:0002616', 'HP:00012345'], similarity_metric='PHENODIGM', limit=10)
print "Found {} cases with score {}".format(len(similar_cases), ", ".join([str(c['score']) for c in similar_cases]))
```

    INFO:root:2018-08-05 09:43:54.771078 GET http://localhost:8080/cva/api/0/cases/phenotypes/similar-cases?limit=10&similarity_metric=PHENODIGM&hpo_ids=HP:0002616&hpo_ids=HP:00012345 Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=777, Date=Sun, 05 Aug 2018 08:43:54 GMT
    INFO:root:Response time : 167 ms


    Found 10 cases with score 0.28867513, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0



```python
# get top 10 cases having any tiered variant shared with a case
similar_cases = cases_client.get_shared_variants_cases_by_case(
    "132", 1, report_event_type=ReportEventType.tiered, limit=10)
print "Found {} cases with shared variants {}".format(
    len(similar_cases), ", ".join([str(len(c['sharedVariants'])) for c in similar_cases]))
```

    INFO:root:2018-08-05 09:43:55.215706 GET http://localhost:8080/cva/api/0/cases/132/1/shared-variants?limit=10&type=tiered Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Transfer-Encoding=chunked, Date=Sun, 05 Aug 2018 08:43:54 GMT
    INFO:root:Response time : 338 ms


    Found 10 cases with shared variants 3, 2, 5, 4, 1, 4, 1, 1, 4, 1



```python
# get top 10 cases having any reported variant shared with case 4108-1
similar_cases = cases_client.get_shared_variants_cases_by_case(
    "132", 1, report_event_type=ReportEventType.reported, limit=10)
if similar_cases:
    print "Found {} cases with shared variants {}".format(
        len(similar_cases), ", ".join([str(len(c['sharedVariants'])) for c in similar_cases]))
else:
    print "No cases found"
```

    INFO:root:2018-08-05 09:43:55.385084 GET http://localhost:8080/cva/api/0/cases/132/1/shared-variants?limit=10&type=reported Server=Apache-Coyote/1.1, Access-Control-Allow-Origin=*, Access-Control-Allow-Headers=x-requested-with, content-type, Access-Control-Allow-Credentials=true, Access-Control-Allow-Methods=GET, POST, OPTIONS, Content-Type=application/json, Content-Length=243, Date=Sun, 05 Aug 2018 08:43:54 GMT
    INFO:root:Response time : 99 ms
    WARNING:root:No cases sharing reported variants  found


    No cases found

