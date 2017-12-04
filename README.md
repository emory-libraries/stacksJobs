# stacksJobs

### Title: Stacks Jobs

### Author: Alex Cooper

### Purpose: Automate stacks data processes

### Dependencies: Can be found in the files directory

----

## Manage Stacks Sets [manage_stacks_sets.sh](https://github.com/Emory-LCS/stacksJobs/blob/master/manage_stacks_sets.sh)

#### Purpose: Run the xmxl and wd scripts from the crontab

```
$bash manage_stacks_sets.sh
```

----

## Manage New Books Sets [manage_new_books_set.sh](https://github.com/Emory-LCS/stacksJobs/blob/master/manage_new_books_set.sh)

#### Purpose: Run the new books scripts from the crontab

```
$bash manage_stacks_sets.sh
```

----

## Stacks Apis [stacks_apis.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/stacks_apis.rb)

#### Purpose: Make Analytics call and parse Analytics response

#### Dependency: stacks.cfg

```
limit=1000
analytics_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports
path_wd=/shared/Emory University Libraries/Reports/LHAMLET/WDforDeletion
path_xmxl_bus=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDBUS
path_xmxl_chem=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDCHEM
path_xmxl_hlth=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDHLTH
path_xmxl_lsc=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDLSC
path_xmxl_musme=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDMUSME
path_xmxl_univ=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDUNIV
path_new=/shared/Emory University Libraries/Reports/LHAMLET/UNIVNEWBKwithUSE
analytics_apikey=[apikey]
alma_bib_apikey=[apikey]
alma_bib_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs
```

----

## New Books Apis [new_books_api.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/new_books_api.rb)

#### Purpose: Make Analytics call and parse Analytics response

#### Dependency: stacks.cfg

```
limit=1000
analytics_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports
path_wd=/shared/Emory University Libraries/Reports/LHAMLET/WDforDeletion
path_xmxl_bus=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDBUS
path_xmxl_chem=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDCHEM
path_xmxl_hlth=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDHLTH
path_xmxl_lsc=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDLSC
path_xmxl_musme=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDMUSME
path_xmxl_univ=/shared/Emory University Libraries/Reports/LHAMLET/XMXLtoWDUNIV
path_new=/shared/Emory University Libraries/Reports/LHAMLET/UNIVNEWBKwithUSE
analytics_apikey=[apikey]
alma_bib_apikey=[apikey]
alma_bib_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs
```

#### Output: addMembers.xml

```
<set><members><member><id>010000690077</id></member></members></set>
```

----

## Create Stacks Items Set [create_stacks_set.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/create_stacks_set.rb)

#### Purpose: Creates set and returns its ID

#### Depnedency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
wd_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/jobs/M157
apikey=[apikey]
```

#### Denepndency: set.xml

#### Output: setId (a file string the set ID)

----

----

## Create New Books Set [create_new_books_set.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/create_new_books_set.rb)

#### Purpose: Creates set and returns its ID

#### Depnedency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
apikey=[apikey]
```

#### Denepndency: set.xml

#### Output: setId (a file string the set ID)

----

## Add Members to Stacks Set [add_barcodes_to_set.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/add_barcodes_to_set.rb)

#### Purpose: Add members to set based on barcodes

#### Dependency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
apikey=[apikey]
```

#### Dependency: setId

#### Dependency: addMembers.xml

----

## Run Change Item Job [run_stacks_job.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/run_stacks_job.rb)

#### Purpose: Run the change items job for Stacks team

#### Dependency: run_a_job.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/jobs/M18
apikey=[apikey]
```

#### Dependency: setId

#### Dependency: one of 7 job.xml

----

## Delete Stacks Set [delete_stacks_set.rb](https://github.com/Emory-LCS/stacksJobs/blob/master/delete_stacks_set.rb)

#### Purpose: Delete the set of items

#### Dependency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
apikey=[apikey]
```

#### Dependency: setId

----
