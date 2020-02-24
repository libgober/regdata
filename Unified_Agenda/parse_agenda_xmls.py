"""
Parsing the Regulatory Agenda into a queriable database

Author(s): Brian Libgober

Last Modified: Oct 13, 2019

"""


import xml.etree.ElementTree as ET
from lxml import etree
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
"""
Explanation:

Useful Reference: https://reginfo.gov/public/xml/REGINFO_XML_Ver10262011.xsd

Each "row" in the XML data is an RIN, which is a rule identification number.
Since we wish to combine XMLs into a single database, we should also identify
RINs via PUBLICATION_ID

Some meta data associated with each RIN is flat, such as the rule title.
Others have a nested structure, such as the legal authorities or the regulatory
actions already taken.

The clearest structure will come from separating these out.

"""

def pprint_xml(element):
    print etree.tostring(element,pretty_print=True)

def clean_element(element):
    'preprocessing step: ETREE xpath selectors yield either elements, none types, or empty strings'
    if element is None:
        return None
    elif element.text is None: 
        return None
    else:
        return element.text.strip()

def generic_info(RIN_INFO):
    #identifiers that are important for all calls
    RIN = RIN_INFO.find("./RIN")
    PUB_ID =  RIN_INFO.find(".//PUBLICATION_ID")
    return RIN, PUB_ID

def identify_publication_id(root):
    IDS = root.findall(".//PUBLICATION_ID")
    ID = np.unique(map(lambda x: x.text,IDS))
    if len(ID)>1:
        raise Error("Assumed only one publication id for each doc")
    return ID[0]

def extract_flat_infos(RIN_INFO):
    """
    pull out the flat information
    """
    RIN, PUB_ID = generic_info(RIN_INFO)
    out = {'RIN' : RIN, 'PUB_ID' : PUB_ID}
    out['AGY_CODE'] = RIN_INFO.find("./AGENCY/CODE")
    out['PARENT_AGY_CODE'] = RIN_INFO.find("./PARENT_AGENCY/CODE")
    out['RULE_TITLE'] = RIN_INFO.find("./RULE_TITLE")
    out['ABSTRACT'] = RIN_INFO.find("./ABSTRACT")
    out['PRIORITY_CATEGORY'] = RIN_INFO.find("./PRIORITY_CATEGORY")
    out['RIN_STATUS'] = RIN_INFO.find("./RIN_STATUS")
    out['RULE_STAGE'] = RIN_INFO.find("./RULE_STAGE")
    out['MAJOR'] = RIN_INFO.find("./MAJOR")
    out['RFA_SECTION_610_REVIEW'] = RIN_INFO.find("./RFA_SECTION_610_REVIEW")
    out['RPLAN_ENTRY'] = RIN_INFO.find("./RPLAN_ENTRY")
    out['ADDITIONAL_INFO'] = RIN_INFO.find("./ADDITIONAL_INFO")
    out['RFA_REQUIRED'] = RIN_INFO.find("./RFA_REQUIRED")
    out['FEDERALISM'] = RIN_INFO.find("./FEDERALISM")
    out['ENERGY_AFFECTED'] = RIN_INFO.find("./ENERGY_AFFECTED")
    out['FURTHER_INFO_URL'] = RIN_INFO.find("./FURTHER_INFO_URL")
    out['PUBLIC_COMMENT_URL'] = RIN_INFO.find("./PUBLIC_COMMENT_URL")
    out['COMPLIANCE_COST'] = RIN_INFO.find("./COMPLIANCE_COST")
    out['PRINT_PAPER'] = RIN_INFO.find("./PRINT_PAPER")
    out['INTERNATIONAL_INTEREST'] = RIN_INFO.find("./INTERNATIONAL_INTEREST")
    out['PROCUREMENT'] = RIN_INFO.find("./PROCUREMENT")
    out["REINVENT_GOVT"] = RIN_INFO.find("./REINVENT_GOVT")
    out["SIC_DESC"] = RIN_INFO.find("./SIC_DESC")
    
    return {key : clean_element(out[key]) for key in out.keys()}

def agency_definitions(root):
    """
    Each RIN is associated with one agency (and also maybe one parent agency)
    While the XML is not "flat", by storing only the AGY CODE and having
    a table with definitions, we can flatten this aspect of the XML.
    
    So this is an example of flattanable XML
    """
    AGENCIES = root.findall("./RIN_INFO/AGENCY")
    PARENT_AGENCIES = root.findall("./RIN_INFO/PARENT_AGENCY")
    foo = set()
    for a,p in zip(AGENCIES,PARENT_AGENCIES):
        entry=map(lambda x: clean_element(a.find(x)),['CODE','NAME','ACRONYM'])  +\
            map(lambda y: clean_element(p.find(y)),['CODE','NAME','ACRONYM'])
        foo.add(tuple(entry))
    out = pd.DataFrame(list(foo),columns=["CODE","NAME","ACRONYM",'PARENT_CODE','PARENT_NAME',"PARENT_ACRONYM"])
    out['PUBLICATION_ID'] = identify_publication_id(root)
    return out    

def legal_authories(RIN_INFO):
    """
    This is truly unflat information. Each RIN may have multiple legal
    authorities.
    
    We will store all these in a long format in a separate table.
    """
    RIN, PUB_ID = generic_info(RIN_INFO)
    AUTHORITIES = RIN_INFO.findall("LEGAL_AUTHORITY_LIST/LEGAL_AUTHORITY")
    out = [{
        "RIN" : clean_element(RIN),
        "PUB_ID" : clean_element(PUB_ID),
        "AUTHORITY" : clean_element(AUTHORITY)} for 
        AUTHORITY in AUTHORITIES]
    return out
    
def parse_timetables(RIN_INFO):
    "The other most important example of really unflat information"
    RIN, PUB_ID = generic_info(RIN_INFO)
    TIMETABLES = RIN_INFO.findall("TIMETABLE_LIST/TIMETABLE")
    out = [{
        "RIN" : clean_element(RIN),
        "PUB_ID" : clean_element(PUB_ID),
        "ACTION" : clean_element(TIMETABLE.find("TTBL_ACTION")),
        "DATE" : clean_element(TIMETABLE.find("TTBL_DATE")),
        "FR_CITATION" :clean_element(TIMETABLE.find("FR_CITATION"))
        } for 
        TIMETABLE in TIMETABLES]
    return out

def parse_contacts(RIN_INFO):
    "Another turns out to be important"
    RIN, PUB_ID = generic_info(RIN_INFO)
    CONTACTS = RIN_INFO.findall("AGENCY_CONTACT_LIST/CONTACT")
    out = [{
        "RIN" : clean_element(RIN),
        "PUB_ID" : clean_element(PUB_ID),
        "FIRST_NAME" : clean_element(CONTACT.find("FIRST_NAME")),
        "LAST_NAME" : clean_element(CONTACT.find("LAST_NAME")),
        "TITLE" : clean_element(CONTACT.find("TITLE")),
        'AGENCY' : clean_element(CONTACT.find("AGENCY/CODE")),
        'PHONE' : clean_element(CONTACT.find("PHONE")),
        'EMAIL' : clean_element(CONTACT.find("EMAIL"))
        } for CONTACT in CONTACTS]
    return out
    
def flatten_list(l):
    flat_list = []
    for sublist in l:
        for item in sublist:
            flat_list.append(item)
    return flat_list



def main(xml_path):
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(xml_path,parser=parser)
    root = tree.getroot()
    RIN_INFOS =  root.findall(".//RIN_INFO")
    #useful, see the tags possible
    set([i.tag for i in tree.findall("*/")])
    #write the main RINS table
    rins = pd.DataFrame(map(extract_flat_infos,RIN_INFOS))
    rins.columns = map(lambda x: x.lower(),rins.columns)
    rins.to_sql("rins","sqlite:///agenda.sqlite",index=False,if_exists="append")
    #this is the list of legal authorities
    authorities = pd.DataFrame(flatten_list(map(legal_authories,RIN_INFOS)))
    authorities.columns = map(lambda x: x.lower(),authorities.columns)
    authorities.to_sql("legal_authorities","sqlite:///agenda.sqlite",index=False,if_exists="append")
    #this is the list of rules 
    timetables = pd.DataFrame(flatten_list(map(parse_timetables,RIN_INFOS)))
    timetables.columns = map(lambda x: x.lower(),timetables.columns)
    timetables.to_sql("timetables","sqlite:///agenda.sqlite",index=False,if_exists="append")
    #this is the list of contacts
    contacts = pd.DataFrame(flatten_list(map(parse_contacts,RIN_INFOS)))
    contacts.columns = map(lambda x: x.lower(),contacts.columns)
    contacts.to_sql("contacts","sqlite:///agenda.sqlite",index=False,if_exists="append")
    #write the agency definitions 
    agency_defs =  agency_definitions(root)   
    agency_defs.columns = map(lambda x: x.lower(),agency_defs.columns)
    agency_defs.to_sql("agency_defn","sqlite:///agenda.sqlite",index=False,if_exists="append")

#here's where we actually run
if __name__=='__main__':
    for xml_path in tqdm(glob("XMLs/*.xml")):
        main(xml_path)
