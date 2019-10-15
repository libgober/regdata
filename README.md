# regdata
A repository for important data sources on the regulatory state. Collaboration welcome. We are working on scripts for downloading and parsing content put out aobut federal rulemaking and related issues in US bureaucratic politics. Ideally, final output will be in the form of sqlite databases that can be easily shared and queried. What follows is notes on data sources that we know about and are working on acquiring.

Because of the constraints on large files, we are investigating options for storing output. Currently we are hosting ad hoc via Dropbox. 

# Authors

- Brian Libgober, Postdoc in Political Science at Yale (brian.libgober@yale.edu).
- Steven Rashin, Postdoc in Government at Harvard.
- Devin Judge-Lord, PhD Candidate in Political Science at UW-Madison.

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
- Federal Energy Regulatory Commission

## Other Wish List Sources

- Meetings
