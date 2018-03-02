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

[Search](#Search-API) [SmartAlerts](#Alerts-API) [Signals](#Signals-API) [Records](#Records-API) [Assets](#Assets-API) [Integrations](#Integrations-API) [Status](#Status-API) [Threat Intel](#Threat-Intel-API) [Signals](#Signals-API) [Patterns](#Patterns-API)

## Search API
-------------------------------------------

**Global Search:**
```
GET:  /api/search?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<INT>]&[offset=<INT>]
```
Returns:

JSON of all hits across data types of Asset, SmartAlert, and Signal

**Signals Search:**
```
GET:  /api/search/signals?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<INT>]&[offset=<INT>]
```
Returns:

JSON of all hits across data types of Asset, SmartAlert, and Signal

**Alert Search:**
```
GET:  /api/search/alerts?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<INT>]&[offset=<INT>]
```
Returns:

JSON of all hits across data types of Asset, SmartAlert, and Signal

**Asset Search:**
```
GET:  /api/search/assetts?q=<query string>&[sort_by=<+ or -><fieldname>]&[limit=<INT>]&[offset=<INT>]
```
Returns:

JSON of all hits across data types of Asset, SmartAlert, and Signal

-------------------------------------------

