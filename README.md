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

[Search](#Search-API) [SmartAlerts](#Alerts-API) [Signals](#Signals-API) [Records](#Records-API) [Assets](#Assets-API) [Integrations](#Integrations-API) [Status](#Status-API) [Threat Intel](#Threat-Intel-API) [Sensors](#Sensors-API) [Patterns](#Patterns-API)

## Search API
-------------------------------------------

**Global Search:**
```
GET:  /api/search?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<int>]&[offset=<int>]
```
Returns:

JSON of all hits across data types of asset, smartalert, and signal inside optional filter params.

**Signals Search:**
```
GET:  /api/search/signals?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<int>]&[offset=<int>]
```
Returns:

JSON of all matching signals inside optional filter params.

**Alert Search:**
```
GET:  /api/search/alerts?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<int>]&[offset=<int>]
```
Returns:

JSON of all matching smartalerts inside optional filter params.

**Asset Search:**
```
GET:  /api/search/assetts?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<int>]&[offset=<int>]
```
Returns:

JSON of all matching assets inside optional filter params.

-------------------------------------------

## SmartAlerts
-------------------------------------------

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


## Records API
-------------------------------------------


## Assets API
-------------------------------------------


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

