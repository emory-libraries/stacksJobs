# stacksJobs

### Title: Stacks Jobs

### Author: Alex Cooper

### Purpose: Automate stacks data processes

### Dependencies: Can be found in the files directory

----

## Manage Stacks Sets

#### Purpose: Run the scripts from the crontab

```
$bash manages_stacks_sets.sh
```

----

## Stacks Apis

#### Purpose: Make analytics call and parse Analytics response

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
analytics_apikey=[apikey]
alma_bib_apikey=[apikey]
alma_bib_url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs
```

#### Output: addMembers.xml

```
<set><members><member><id>010000690077</id></member></members></set>
```

----

## Create Stacks Items Set

#### Purpose: Creates set and returns its ID

#### Depnedency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
apikey=[apikey]
```

#### Denepndency: set.xml

----

## Add Memebers to Stacks Set

#### Purpose: Add members to set based on barcodes

#### Dependency: create_set.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets
apikey=[apikey]
```

#### Dependency: addMembers.xml

----

## Run Change Item Job

#### Purpose: Run the change items job for Stacks team

#### Dependency: run_a_job.cfg

```
url=https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/jobs/M18
apikey=[apikey]
```

#### Dependency: one of 6 job.xml

----
