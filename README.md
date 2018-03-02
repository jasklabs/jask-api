### JASK TRIDENT API v.01 (Not Versioned)
===========================================

# JASK API Global Interaction Rules
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

V.01 of this DOC will cover the following APIs and basic functionality for each:

[Search](#search-api) [SmartAlerts](#alerts-api) [Signals](#signals-api) [Assets](#assets-api) [Integrations](#integrations-api) [Status](#status-api) [Threat Intel](#threat-intel-api) [Sensors](#sensors-api) [Patterns](#patterns-api)

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

**Records Related to Signal Enrichment:**
```
GET:  /api/alert/[SIGNAL ID]/records/all
```
Returns:

Returns JSON object containing all records (logs) conected with a signal if available. "all" may be substituted with a specific record type.

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

**Asset's Related Assets**
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

**Records Related to Signal Enrichment:**
```
GET:  /api/alert/[SIGNAL ID]/records/all
```
Returns:

Returns JSON object containing all records (logs) conected with a signal if available. "all" may be substituted with a specific record type.

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

## Integrations API
-------------------------------------------


## Status API
-------------------------------------------

## Threat Intel API
-------------------------------------------


## Sensors API
-------------------------------------------

## Patterns API
-------------------------------------------

