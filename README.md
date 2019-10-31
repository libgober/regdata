# regdata
A repository for important data sources on the regulatory state. Collaboration welcome. We are working on scripts for downloading and parsing content put out aobut federal rulemaking and related issues in US bureaucratic politics. Ideally, final output will be in the form of sqlite databases that can be easily shared and queried. What follows is notes on data sources that we know about and are working on acquiring.

Because of the constraints on large files, we are investigating options for storing output. Currently we are hosting ad hoc via Dropbox. 

# Authors

- Brian Libgober, Postdoc in Political Science at Yale (brian.libgober@yale.edu).
- Steven Rashin, Postdoc in Government at Harvard.
- Devin Judge-Lord, PhD Candidate in Political Science at UW-Madison.

## Data Sources
| ﻿Website                                  | Link to data                                                                                        | What does it have?                                                               | Notes                                                                                     | Uses                         |
|------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|------------------------------|
| Comment Text                             |                                                                                                     |                                                                                  |                                                                                           |                              |
| Regulations.gov                          | https://regulationsgov.github.io/developers/console/#!/documents.json/documents_get_0               | Comments from executive agencies                                                 | Need an API key.  Keys are restricted and may be deactivated without any notice.          | Studying comment behavior    |
| CFTC                                     | https://comments.cftc.gov/PublicComments/ReleasesWithComments.aspx                                  | Comments on CFTC regulations                                                     | Have to scrape                                                                            |                              |
| Federal Communications Commission        | https://www.fcc.gov/ecfs/                                                                           | Comments on FCC regulations                                                      | Have to scrape.  Use limits and offset parameters to go beyond the first page             |                              |
| Federal Reserve                          | https://www.federalreserve.gov/apps/foia/proposedregs.aspx                                          | Comments on Federal Reserve regulations                                          | Have to scrape. Change “ViewComments” to “ViewAllComments” in the URL to get all comments |                              |
| SEC                                      | https://www.sec.gov/rules/proposed.shtml                                                            | Comments on regulations issued by the SEC                                        | Have to scrape                                                                            |                              |
| Rule Text                                |                                                                                                     |                                                                                  |                                                                                           |                              |
| *Federal Register*                       | https://www.federalregister.gov/developers/api/v1                                                   | Text form of all notices, proposed rules, and final rules                        | Not rate limited                                                                          |                              |
| Rule Metadata                            |                                                                                                     |                                                                                  |                                                                                           |                              |
| Davis Polk Dodd Frank Tracker            | https://www.regulatorytracker.com/regtracker/LoginRequiredPage.action                               | A tracker with information on Dodd-Frank regulations                             | Need an account                                                                           | Analysis of Dodd-Frank rules |
| Federal Reserve Press Releases           | https://www.federalreserve.gov/newsevents/pressreleases.htm                                         | Press releases from the federal reserve                                          |                                                                                           |                              |
| SEC Press Releases                       | https://www.sec.gov/news/pressreleases?year=All&month=All&items_per_page=100&page=1                 | Press releases from the federal reserve                                          | RSS code available by a button on the top of the table                                    |                              |
| Unified Agenda                           | https://www.govinfo.gov/collection/unified-agenda?path=/gpo/Unified%20Agenda/1998/GPO-UA-1998-11-09 | Machine readable versions of the unified agenda in raw .txt form and in XML form |                                                                                           |                              |
|                                          |                                                                                                     |                                                                                  |                                                                                           |                              |
|                                          | https://www.reginfo.gov/public/do/eAgendaXmlReport                                                  |                                                                                  |                                                                                           |                              |
|                                          |                                                                                                     |                                                                                  |                                                                                           |                              |
| Corporate Finance Data                   |                                                                                                     |                                                                                  |                                                                                           |                              |
| IRS-990 Forms                            | https://www.irs.gov/charities-non-profits/copies-of-eo-returns-available                            | IRS-990 Forms for financial information on nonprofits                            |                                                                                           |                              |
| Wharton Research Data Service            | https://wrds-web.wharton.upenn.edu/wrds/index.cfm?                                                  | Databases such as Compustat on corporate financial activity                      | Need an institutional account                                                             |                              |
| Participants in the Policymaking Process |                                                                                                     |                                                                                  |                                                                                           |                              |
| Foreign Agent Registration Act           | https://efile.fara.gov/ords/f?p=1235:10                                                             | Text of metadata on foreign registrations, PDFs of contacts                      | Rate limited to 5 requests every 10 seconds                                               |                              |
| Open Secrets Lobbying Database           | https://www.opensecrets.org/bulk-data/downloads                                                     | Digital versions of lobbying reports and campaign finance data                   | Need to register for an Open Secrets account                                              |                              |
| CFTC meetings                            | https://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings                                    | Meeting logs for external meetings                                               | Must be scraped                                                                           |                              |

## Federal Register

There are two important potential sources:

- XML bulk data is available from https://www.govinfo.gov/bulkdata/FR
- Federal Register API gives meta data and plain text back to 1994.

CURRENT STATUS
  
- JSON lines formatted meta data of all rules from January, 1994 to mid-October, 2019. https://www.dropbox.com/s/zlgyz2lclgrgz84/2019_10_13.jl?dl=0

## Unified Agenda of Regulatory and Deregulatory Actions

Major source is XML versions available from 1995 until present

https://www.reginfo.gov/public/do/eAgendaXmlReport

CURRENT STATUS

- Bash script to download all these XMLs is in the directory.
- Partial transformation to SQLITE database is complete. Available here: https://www.dropbox.com/s/wnw5husrx7lpagw/agenda.sqlite?dl=0

## Regulations.gov (for comments)

Agencies that do not host comments on Regulations.gov:

- Federal Reserve System
- Federal Communications Commission

## Other Wish List Sources

- Meetings
