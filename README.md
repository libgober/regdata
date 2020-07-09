# regdata
A repository for important data sources on the regulatory state. Collaboration welcome. We are working on scripts for downloading and parsing content put out aobut federal rulemaking and related issues in US bureaucratic politics. Ideally, final output will be in the form of sqlite databases that can be easily shared and queried. What follows is notes on data sources that we know about and are working on acquiring.

Because of the constraints on large files, we are investigating options for storing output. Currently we are hosting ad hoc via Dropbox. 

# Authors

- Brian Libgober, Postdoc in Political Science at Yale (brian.libgober@yale.edu).
- Steven Rashin, Visiting Scholar at Harvard (steven_rashin@radcliffe.harvard.edu).
- Devin Judge-Lord, PhD Candidate in Political Science at UW-Madison (JudgeLord@wisc.edu).

## Data Sources
To access the data discussed in our paper 'Data and Methods Analyzing Special Interests Influence in Rulemaking' see the file data_sources.md in the menu above.

## Federal Register

There are two important potential sources:

- [XML bulk data](https://www.govinfo.gov/bulkdata/FR)
- Federal Register API gives meta data and plain text back to 1994. 

CURRENT STATUS
  
- [JSON lines formatted meta data of all rules from January, 1994 to mid-October, 2019](https://www.dropbox.com/s/zlgyz2lclgrgz84/2019_10_13.jl?dl=0)
- [Examples using the R package `federalregister`](https://github.com/judgelord/rulemaking/blob/master/functions/federalregister-search.R) [TODO: Make a tutorial for this]

## Unified Agenda of Regulatory and Deregulatory Actions

- [XML versions available from 1995 until present](https://www.reginfo.gov/public/do/eAgendaXmlReport)

CURRENT STATUS

- Bash script to download all these XMLs is in the directory.
- [Partial transformation to SQLITE database is complete.](https://www.dropbox.com/s/wnw5husrx7lpagw/agenda.sqlite?dl=0)
- [Transformed to Rdata. Some errors corrected for 2000-2018](https://github.com/judgelord/rulemaking/blob/master/data/UnifiedAgenda.Rdata)
```
 [1] "ABSTRACT"                
 [2] "ADDITIONAL_INFO"         
 [3] "AGENCY"                  
 [4] "AGENCY_CONTACT_LIST"     
 [5] "ANPRM"                   
 [6] "ANPRMcomment"            
 [7] "ANPRMfedreg"             
 [8] "CFR_LIST"                
 [9] "CHILD_RIN_LIST"          
[10] "COMPLIANCE_COST"         
[11] "ENERGY_AFFECTED"         
[12] "EO_13771_DESIGNATION"    
[13] "FEDERALISM"              
[14] "FINAL"                   
[15] "FINALeffective"          
[16] "FINALfedreg"             
[17] "FINALjudicial"           
[18] "FINALstatutory"          
[19] "FURTHER_INFO_URL"        
[20] "GOVT_LEVEL_LIST"         
[21] "IFR"                     
[22] "IFRcomment"              
[23] "IFReffective"            
[24] "IFRfedreg"               
[25] "INTERNATIONAL_INTEREST"  
[26] "JudicialFinal"           
[27] "JudicialNPRM"            
[28] "LEGAL_AUTHORITY_LIST"    
[29] "LEGAL_DLINE_LIST"        
[30] "LEGAL_DLINE_OVERALL_DESC"
[31] "MAJOR"                   
[32] "NAICS_LIST"              
[33] "NPRM"                    
[34] "NPRMcomment"             
[35] "NPRMfedreg"              
[36] "NPRMjudicial"            
[37] "NPRMstatutory"           
[38] "PARENT_AGENCY"           
[39] "PARENT_RIN"              
[40] "PRINT_PAPER"             
[41] "PRIORITY_CATEGORY"       
[42] "PROCUREMENT"             
[43] "PUBLIC_COMMENT_URL"      
[44] "REINVENT_GOVT"           
[45] "RELATED_AGENCY_LIST"     
[46] "RELATED_RIN_LIST"        
[47] "RFA_REQUIRED"            
[48] "RFA_SECTION_610_REVIEW"  
[49] "RIN"                     
[50] "RIN_STATUS"              
[51] "RPLAN_ENTRY"             
[52] "RPLAN_INFO"              
[53] "RULE_TITLE"              
[54] "SIC_DESC"                
[55] "SMALL_ENTITY_LIST"       
[56] "SNPRM"                   
[57] "SNPRMcomment"            
[58] "SNPRMfedreg"             
[59] "STAGE"                   
[60] "StatutoryFinal"          
[61] "StatutoryNPRM"           
[62] "TIMETABLE_LIST"          
[63] "UNFUNDED_MANDATE_LIST"   
[64] "UnifiedAgendaDate"       
[65] "WITHDRAWAL" 
```

## Office of Information and Regulatory Affairs (ORIA) Reports

- [XML versions available from 1981 until present](http://www.reginfo.gov/public/do/XMLReportList)
- [Transformed to Rdata. Some errors corrected.](https://github.com/judgelord/rulemaking/blob/master/data/OIRA.Rdata)
```
 [1] "AGENCY_CODE"                    
 [2] "ANPRM_COMPLETED"                
 [3] "ANPRM_PUBLISHED"                
 [4] "ANPRM_RECIEVED"                 
 [5] "DATE_COMPLETED"                 
 [6] "DATE_PUBLISHED"                 
 [7] "DATE_RECEIVED"                  
 [8] "DECISION"                       
 [9] "DODD_FRANK_ACT"                 
[10] "ECONOMICALLY_SIGNIFICANT"       
[11] "EXPEDITED_REVIEW"               
[12] "FEDERALISM_IMPLICATIONS"        
[13] "FINAL_COMPLETED"                
[14] "FINAL_PUBLISHED"                
[15] "FINAL_RECIEVED"                 
[16] "HEALTH_CARE_ACT"                
[17] "HOMELAND_SECURITY"              
[18] "IFR_COMPLETED"                  
[19] "IFR_PUBLISHED"                  
[20] "IFR_RECIEVED"                   
[21] "INTERNATIONAL_IMPACTS"          
[22] "LEGAL_DEADLINE"                 
[23] "MAJOR_OIRA"                     
[24] "NPRM_COMPLETED"                 
[25] "NPRM_PUBLISHED"                 
[26] "NPRM_RECIEVED"                  
[27] "REGULATORY_FLEXIBILITY_ANALYSIS"
[28] "RIN"                            
[29] "SMALL_ENTITIES_AFFECTED"        
[30] "SNPRM_COMPLETED"                
[31] "SNPRM_PUBLISHED"                
[32] "SNPRM_RECIEVED"                 
[33] "STAGE"                          
[34] "TCJA"                           
[35] "TITLE"                          
[36] "UNFUNDED_MANDATES"
```

## Regulations.gov (rule metadata and comments)

- Metadata for all rules, proposed rules, and notices ([.Rdata](https://github.com/judgelord/rulemaking/blob/master/data/AllRegsGovRules.Rdata))
- R script to scrape attachments ([all file formats](https://github.com/judgelord/rulemaking/blob/master/functions/regulations-gov-get-attachments.R), pdf only)
```
 [1] "agencyAcronym"           
 [2] "allowLateComment"        
 [3] "attachmentCount"         
 [4] "commentDueDate"          
 [5] "commentStartDate"        
 [6] "docketId"                
 [7] "docketTitle"             
 [8] "docketType"              
 [9] "documentId"              
[10] "documentStatus"          
[11] "documentType"            
[12] "frNumber"                
[13] "numberOfCommentsReceived"
[14] "openForComment"          
[15] "postedDate"              
[16] "rin"                     
[17] "title" 
```

- Metadata for comments (sample, excluding attachment text)([.Rdata](https://github.com/judgelord/rulemaking/blob/master/data/allcomments-sample.Rdata))
- [Scraper for comments posted to regulations.gov as attachments](https://github.com/judgelord/rulemaking/blob/master/functions/regulations-gov-get-attachments.R) [TODO: UPDATE THIS, MAKE IT INTO A TUTORIAL, ADD VERSION THAT DOES NOT REQUIRE API KEY]

## Agencies that do not host comments on Regulations.gov:

- Federal Reserve System
- Federal Communications Commission
- Federal Energy Regulatory Commission ([FERC Document Scraper](https://judgelord.github.io/correspondence/functions/DOE_FERC-scraper.html))

## Other Wish List Sources

- Meetings
