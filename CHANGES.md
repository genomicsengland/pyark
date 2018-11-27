v3.0.2
======

* Bugfixes.....
* Allow building custom endpoints from the main client

v3.0.1
======

* Added endpoints to search panels and disorders by regex

v3.0.0
======

* Added new endpoints about entities in backend
* Still more Pandas integration
* Added `**params` all over the place, so we can use parameter names as they are in pyark
* Test reports for builds
* Align version with backend

v2.0.4
======

* Support for versioning of entities (ie: panels and disorders)
* Integration of pandas series instead of lists for entities results
* Better integration of Pandas data frames:
    - MultiIndex created for each dataframe depending on the query performed to obtain the data
    - Multiple queries supported in one go and data frame concatenation is provided out of the box

v2.0.3
======

* Avoid flattening results as it introduces a dependency on the format of the output

v2.0.2
======

* Added endpoint to get disorders
* Panels client renamed to entities client as it has a wider scope now
* Support for Python3 and Python 2

v2.0.1
======

* Update to models version 7.1.12
* Change of `ReportEventType.genomics_england_tiering`

v2.0.0
======

* Alignemnt of versioning (only major and minor versions) to backend

v0.10.0
======

* Added endpoint to get cases having shared variants
* Refactored endpoints that fetch gene summaries
* Updated to latest gel report models

v0.9.0
======

* Changed endpoints for report events and cases
* Hidden some fields and methods to end user
* Added endpoint to fetch genes by panel

v0.5.0
======

* Support for cases similarity queries

v0.4.0
======

* Paginated endpoints return a number when `count=True`

v0.3.0
======

* Added endpoint to fetch lift overs
* Added endpoint to paginate over cases

v0.2.0
======

* Support for pandas data frames in summary endpoints
* Update of multiple endpoints

v0.1.0
======

* First release
