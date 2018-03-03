# JASK TRIDENT API v.01 
-------------------------------------------

## JASK API Global Interaction Rules
-------------------------------------------
**URL STRUCTURE**

Access to your JASK data is provided on a per cluster basis. 

Please replace [CUSTOMER] with your organizations instance name in the universal base URL prepended to all examples:
```
https://[CUSTOMER].portal.jask.ai:443/api/
```
**AUTHENTICATION**

Authentication is currently performed via GET variables consisting of username and API key appended to the end of all examples: 
```
?username=[USERNAME]&api_key=[APIKEY]
```
You can retrieve your personal API key from the following URL under the "Profile" tab:
```
https://[CUSTOMER].portal.jask.ai/config 
```
**API TOOLS**

This repoistory contains python tools to interface with the most commonly utilized API endpoints (Search, Threat Intel, Etc) located in */jask-api/api-tools*

**SCOPE**

V.01 of this DOC will cover the following APIs and basic functionality for each (*API Subject To Change Without Notice*)

*A thank you to @kbandla for work on [APTnotes](https://github.com/kbandla/APTnotes) provided to test TI ingest here.*

-------------------------------------------
**[Search](#search-api) - [SmartAlerts](#alerts-api) - [Signals](#signals-api) - [Assets](#assets-api) - [Integrations](#integrations-api) - [Status](#status-api) - [Threat Intel](#threat-intel-api) - [Sensors](#sensors-api) - [Patterns](#patterns-api)**

-------------------------------------------
## Search API
-------------------------------------------

JASK Search "query string" is compared to all fields across the selected context (All, Signals, Alerts or Assets), query examples could be IP addresses, Alert Names, or Countries, ISP names, etc). 

Comparision takes place in Elastic Search using [standard analyzer tokenization](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html). 

A field may be specifed as well to restrict search results. 

**Search Query Modifiers for All Search Endpoints**

*Search Query String:*
```
FORMAT: &q=<search query> 

EXAMPLE: &q=104.236.47.73 (Return elements matching "104.236.47.73" in any field)

EXAMPLE: &q=id:2bd18a03-9252-3cf9-a401-1de0fc01cbe4 (Returns elements with "id" fields matching "2bd18a03-9252-3cf9-a401-1de0fc01cbe4")
```

*Sort by (accending or decending) a given return field:*
```
FORMAT: &sort_by=<- or +><fieldname> 

EXAMPLE: &sort_by=-timestamp (sort results by timestamp decending)
```

*Limit Search Results* 
```
FORMAT: &limit=<int> 

EXAMPLE: &limit=<40> (Limit return to first 40 results)
```

*Offset Search Results (For Pagination)*
```
FORMAT: &offset=<int> 

EXAMPLE: &offset=<41> (Start Results from #41)
```

**Global Search:**

```
GET:  /api/search?q=<query string>
```
Returns:

JSON of all hits across data types of asset, smartalert, and signal inside optional filter params.

**Signals Search:**
```
GET:  /api/search/signals?q=<query string>
```
Returns:

JSON of all matching signals inside optional filter params.

**Alert Search:**
```
GET:  /api/search/alerts?q=<query string>
```
Returns:

JSON of all matching smartalerts inside optional filter params.

**Asset Search:**
```
GET:  /api/search/assets?q=<query string>
```
Returns:

JSON of all matching assets inside optional filter params.

-------------------------------------------

## Alerts API
-------------------------------------------
Alerts API references SmartAlerts, or Insights, which are the highest level abstractions in JASK SIEM consisting of multiple signals, and records and relating to one or more assets. 

**Full Alert Details:**
```
GET:  /api/alert/[ALERT ID]
```
Returns:

Full JSON of alert and relevant signals and assets.

**Alert History:**
```
GET:  /api/alert/[ALERT ID]/history
```
Returns:

Returns object containing history of alert if available.

**Alert Comments View and Update:**
```
GET:  /api/alert/[ALERT ID]/comments

POST: /api/alert/comment/<int:comment_id> 
```
Returns:

GET Returns list of alert comments and comment id's. 
POST Updates or adds comments to a specified alert. 

**Alert Enrichments:**
```
GET:  /api/alert/[ALERT ID]/enrichment
```
Returns:

Returns object containing alert enrichment data if available.

**Customer Alert Counts:**
```
GET:  /api/alert/count  
```
Returns:

Returns the total count of alerts over 2/7/30 days and all time for your organization.

**Customer Alert Assignees (JASK Users):**
```
GET:  /api/alert/assignees 
```
Returns:

Returns a list of users and associated ID numbers to whom alerts can be assigned in your organization.

## Signals API
-------------------------------------------
Signals API references signals in JASK which are created when records exhibit suspicious properties and mate with patterns or other detection logic. 

**Full Signal Detail:**
```
GET:  /api/signal/[SIGNAL ID]
```
Returns:

Returns JSON of full signal detail, category, type, and other metadata.

**Signal Enrichments:**
```
GET:  /api/alert/[SIGNAL ID]/enrichment
```
Returns:

Returns object containing signal enrichment data if available.

**Records Related to Signal:**
```
GET:  /api/alert/[SIGNAL ID]/records/<record_type> (<record_type> is either specific such as "dns" or "all")
```
Returns:

Returns JSON object containing all records (logs) conected with a signal if available.

**Customer Signal Counts:**
```
GET:  /api/signal/count  
```
Returns:

Returns the total count of signals over 2/7/30 days and all time for your organization.

## Assets API
-------------------------------------------
Assets API references the device, user, or application involved in an activity inside our outside of the corporate network. This Asset is created through correlations in records and is the subject of alerts and signals. 

**Full Asset Detail:**
```
GET:  /api/asset/[ASSET ID]
```
Returns:

Returns JSON of full asset detail, risk score, source, related assets, and other data.

**Full Asset Detail by IP:**
```
GET:  /api/asset/ip/[ASSET IPv4]
```
Returns:

Returns JSON of full asset detail, risk score, source, related assets, and other data.

**Asset Metadata:**
```
GET:  /api/asset/[ASSET ID]/metadata
```
Returns:

Returns JSON of asset metadata provided through import, correlation, or manual update if available.

**Asset Metadata by IP:**
```
GET:  /api/asset/ip/[ASSET IPv4]/metadata
```
Returns:

Returns JSON of asset metadata provided through import, correlation, or manual update if available.

**Asset Historic Risk**
```
GET:  /api/asset/[ASSET ID]/historic_risk/<int> (int = days to search retroactively)
```
Returns:

Returns JSON of historic risk scores as well as the timestamp they were applied to the asset if available.

**Related Assets**
```
GET:  /api/asset/[ASSET ID]/related_assets
```
Returns:

Returns an object containing other assets determined to be related to the subject via correlation, ML, or manual entry. 

**Asset Change History and Audit Log:**
```
GET:  /api/asset/[ASSET ID]/history
GET:  /api/asset/[ASSET ID]/auditlog
```
Returns:

Returns an object containing the change history or audit log (user making changes) for a given asset over time, including new/old values and dates. 

**Customer Active Asset List:**
```
GET:  /asset/active/<asset_type> (asset_type must be defined, such as "ip") 
```
Returns:

Returns the total count of active assets over 2/7/30 days and all time for your organization.

**Customer Whitelisted Asset List:**
```
GET:  /asset/whitelisted 
```
Returns:

Returns the list of assets which have been whitelisted in JASK by the security team in your organization.

**Customer Riskiest Asset List:**
```
GET:  /asset/riskiest 
```
Returns:

Returns the list of assets with the highest risk score's over a user defined period of time (defined in JASK application)

## Status API
-------------------------------------------
Status API endpoints check for and ensure the health of your JASK ASOC platform.

**JASK Dashboard Counts:**
```
GET:  /api/dashboard/counts
```
Returns:

Returns a JSON of the total flow records and total over all records for an organization, useful for tracking deltas and ingestion perfomance.

**List JASK Users:**
```
GET:  /api/user
```
Returns:

Returns a list of JASK users and their activity records, RBAC, and MFA status, and other details.

**List JASK Sensors:**
```
GET:  /api/sensor
```
Returns:

Returns a list of JASK sensors and their current status, records per second throughput, configs and other details. 


## Threat Intel API
-------------------------------------------
Threat Intelligence API endpoints and helper tools will help ingest and manage threat intel sources relevant to your security team for correlation inside of the JASK platform. 

**Threat Intel Sources:**
```
GET:  /api/intelligence/sources
```
Returns:

Returns a list of imported threat intelligence sources, name of the feed, current count of IOC's and date last modified. 

**Threat Intel Scores:**
```
GET:  /api/intelligence/scoring
```
Returns:

Returns a list of weighting in the form of scores to be applied when a threat intelligence match is made to a given object (example, hash, hostname or url)

**Threat Intel Scoring:**
```
GET:  /api/intelligence/scoring
```
Returns:

Returns a list of weighting in the form of scores to be applied when a threat intelligence match is made to a given object (example, hash, hostname or url)

**Threat Intel CSV Imports:**
```
GET:  /api/intelligence/csvimport
GET:  /api/intelligence/csvimport/[IMPORT ID]
```
Returns:

Returns a list of csvimports containing filename, ID, list of indicators and observables and timestamp of import. Specific details can be retrieved by appending the report ID. 

*Please Utilize the UX/UI or attached Python Tool (/api-tools/sample_intel_api.py) for conducting CSV Imports* 

## Sensors API
-------------------------------------------
Sensor API endpoints allow for granular detail visibility into sensor performance and details.

**List of Sensors:**
```
GET:  /api/sensor
```
Returns:

Returns a list of JASK sensors and their current status, records per second throughput, configs and other details. 

**List of Sensor Errors:**
```
GET:  /api/sensor/error
```
Returns:

Returns a list of error states reported by all connected JASK Sensors.

**Full Sensor Detail:**
```
GET:  /api/sensor/[SENSOR ID]
```
Returns:

Returns a full list of details on a specific sensor including flow data, versioning, and configuration information.

**Sensor History:**
```
GET:  /api/sensor/[SENSOR ID]/history
```
Returns:

Returns a full list history of sensor configuration changes with all details and timestamps so as to identify deltas. 

**Sensor Errors:**
```
GET:  /api/sensor/[SENSOR ID]/error
```
Returns:

Returns a list of error states returned by the specific sensor ID.


## Patterns API
-------------------------------------------
Pattern is the name used to reference detection logic in JASK, the Patterns API enable idenficiation, enablement and manipulation of these rulesets. 

**List of Patterns:**
```
GET:  /api/pattern                (Returns all)
GET:  /api/pattern/[PATTERN TYPE] (Returns a subset based on type such as "match")
```
Returns:

Returns a list of JASK detection logic, their current enabled state, description, category and other details.

**Pattern Status:**
```
GET:  /api/pattern/status
```
Returns:

Returns the number of disabled, enabled and total paterns as well as current matching engine status. 

**Full Pattern Details:**
```
GET:  /api/pattern/[PATTERN TYPE]/[PATTERN ID]
```
Returns:

Returns a JSON of detailed elements of a patern including description, expression, last update and audit info as well as source. 

**Enable or Disable Pattern:**
```
PUT:    /api/pattern/[PATTERN TYPE]/[PATTERN ID]/enable (enables pattern)
DELETE: /api/pattern/[PATTERN TYPE]/[PATTERN ID]/enable (disables pattern)
```
Returns:

Either Enables or Disables a specific pattern based upon type and ID specification.  

