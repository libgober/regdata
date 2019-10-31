#############################
#
# Scraper for:
# All Federal Reserve Dodd-Frank Rules 
#
##########################

# Note this script takes hours to run 
# First go to 
# kenbenoit.net/how-to-batch-convert-pdf-files-to-text/ for install instructions
# We use this later to convert pdfs to text

setwd('')

library(rvest)
library(xml2)
library(XML)
library(stringr)
library(stringi)
library(readr)
library(tidyverse)

html <- read_html("http://www.federalreserve.gov/apps/foia/dfproposals.aspx") #download the HTML

links <- html %>% html_nodes("a") %>% html_attr("href")

links <- links[grepl(pattern = "ViewComments", ignore.case = T, x = links)]

#creates a functional link

full_links<-c(paste("http://www.federalreserve.gov/apps/foia/", links, sep="")) 

df_info<-data.frame(
  link = character(),
  reg = character(),
  num_comments = character(),
  stringsAsFactors=F
)

df_info[1:length(full_links),]<-"NA"
all_comment_links<-list()
index=1

#Now loop through each link and get information about how many regulations are there
for(link in full_links[1:10]){
  
  #get Federal Reserve R number for each regulation
  reg<-str_split(link, "doc_id=")[[1]][2]
  reg<-str_match(reg, "\\w{1,3}%2D\\d{4,6}")[1,1]
  reg<-gsub('%2D', "-", reg)
  
  #save to data frame
  df_info$reg[index]<-reg
  
  #now view all comments
  html <- read_html(link) 
  embedded_links<-html %>% html_nodes("a") %>% html_attr("href")
  
  #filter list so we only see the View All link.  Need this so we scrape all pages not just first
  View_All_Links <- embedded_links[grepl(pattern = "ViewAllComments", embedded_links, ignore.case = T)]
  
  #test whether there are any comments, if none there will be no view all link
  if(identical(View_All_Links, character(0))==F){
    df_info$link[index]<-c(paste("http://www.federalreserve.gov/apps/foia/", View_All_Links, sep=""))
    
    #get num of comments by counting incidences of .pdf.  need to do t/f first, then which ones are true, then length of that
    jumbled_text<-html %>% html_text()
    splitter<-str_match_all(pattern = "Displaying 1 to \\d{1,2} of \\d{1,}", jumbled_text)[[1]][1,1]
    df_info$num_comments[index]<-str_match_all(string = splitter, pattern = "\\d{1,}$")[[1]][1,1]
  } else {
    #If no comments, say so
    df_info$num_comments[index]<-0
    #Get rid of link so we don't use it again
    df_info$link[index]<-"NO COMMENTS"
  }
  #add to index so that we can keep slotting info correctly
  index = index+1
}

#now loop through the links and download all the FR comments

index=1
#link = df_info$link[8]

links_to_comments <- data.frame(
  links = character(),
  nms = character(),
  stringsAsFactors=F
)

for (link in df_info$link[1:10]){
  print(link)
  
  if(link=="NO COMMENTS"){
    cat("Skipping because there are no comments")
    next
  }
  
  all_comments<-read_html(link)
  
  files <- all_comments %>% html_nodes("a") %>% html_attr("href") 
  
  nms <- all_comments %>% html_nodes("a") %>% html_text() #FIX THIS
  
  # Create a temporary data frame with the link and its title
  temporary.data.frame <- data.frame(cbind(files, nms), stringsAsFactors = F)
  temporary.data.frame <- temporary.data.frame[grepl(pattern = "SECRS", x = temporary.data.frame$files),]
  temporary.data.frame <- temporary.data.frame[!grepl("PDF Reader", temporary.data.frame, ignore.case = TRUE),]
  temporary.data.frame <- temporary.data.frame[!grepl("attached file \\(PDF\\)", temporary.data.frame, ignore.case = TRUE),]

  temporary.data.frame$links <- c(paste("http://www.federalreserve.gov", temporary.data.frame$files, sep=""))
  temporary.data.frame$files <- NULL
  
  links_to_comments <- rbind(links_to_comments, temporary.data.frame)
  index=index+1
}

#save(links_to_comments, file="dfs.RData")
#load("dfs.RData")


#Now loop through the links to download the files

for(files_to_download in dfs$links){
  
  print(files_to_download)
  
  #We make sure we haven't already downloaded the file
  files_already_downloaded <- split(as.character(unlist(strsplit(Sys.glob("*.pdf"), "_sep_"))), 1:length(unlist(strsplit(Sys.glob("*.pdf"), "_sep_"))) %% 2 == 0)$`TRUE`
  
  split_link <- str_match(files_to_download, "[^/]+$")[1,1]
  
  if (split_link %in% files_already_downloaded){
    print("Already Downloaded")
    next
  } else {
    
    name <- str_match(string = files_to_download, pattern = "[^/]+$")[1,1] #need a name, we're using everything after final slash
    name1 <- links_to_comments$nms[which(links_to_comments$links==files_to_download)]
    
    #create franken name beceause we need both the end info and the actual persons name
    
    name <- c(paste(name1, "_sep_", name, sep=""))
    
    #Download the actual file
    download.file(files_to_download, mode = "wb", destfile = name)
    
    #Break between each iteration
    Sys.sleep(1.5)
  }
}


#convert the files to txt using pdftotext.  see kenbenoit.net/how-to-batch-convert-pdf-files-to-text/ for install instructions
#replace  spaces with underscores if you don't next line will fail
system('FILES=*.pdf; for f in $FILES; do mv "$f" "${f// /_}"; done') 
system('FILES=*.pdf; for f in $FILES; do echo "Processing $f file..."; pdftotext -enc UTF-8 $f; done; IFS=$SAVEIFS')

#create blank dataframe to fill
DF_Comments<-data.frame(
  rule=character(),
  name = character(),
  organization = character(),
  day=integer(),
  month=integer(),
  year=integer(),
  comment=character(),
  file_link=character(),
  stringsAsFactors=FALSE
)

#load dataframe with NAs because R is a pain in the ass when it comes to dataframes
DF_Comments[1:length(links_to_comments$links),]<-"NA"

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

index=1

for (file in Sys.glob("*.txt")){
  print(file)
  
  txt<-iconv(read_file(file), to='UTF-8-MAC', sub='byte') #load and covert to UTF-8
  txt<-gsub("\n", " ", txt) #get rid of some formatting
  txt<-gsub("[\\]", "", txt) #no backslashes
  txt<-gsub("[a-zA-Z0-9]{30,}", "",txt) #get rid of any string over 30 characters
  #txt<-gsub("\\w*\\d\\w*", "",text) #no words with digits, may not want this 
  txt<- gsub("\\s{2,}"," ", txt) #replace multiple spaces with single space
  txt<-trim(txt)
  
  end_matter<-strsplit(file, "_sep_")[[1]][2]
  end_matter<-gsub(".txt", "", end_matter)
  
  download_link<-dfs$links[which(dfs$end_link==c(paste(end_matter, ".pdf", sep="")))]
  DF_Comments$file_link[index]<-download_link
  #year<-str_match(download_link, pattern = '\\d{4}')[1,1]
  #back1<-strsplit(download_link, "/SECRS/\\d{4}/")[[1]][2]
  #month<-strsplit(download_link, "/")[[1]][6]
  
  name <- strsplit(file, "_\\(")[[1]][1]
  name<-capture.output(cat(name)) #no backslashes
  DF_Comments$name[index]<-name
  
  date = str_match(string = download_link, pattern = "\\d{8}")[1,1] #lazy way but works because date first
  date_col<-read.fwf(textConnection(as.character(date)), widths=rep(2,4), colClasses = 'numeric', header=FALSE) #complicated wat to parse the date into columns
  
  month<-date_col[1,3] #take cols of the frame we created for date
  day<-date_col[1,4]
  year<-as.integer(c(paste(date_col[1,1], date_col[1,2], sep="")))
  
  rule<-strsplit(end_matter, "_")[[1]][1]
  DF_Comments$rule[index]<-rule #slot everything in the dataframe
  DF_Comments$day[index]<-day
  DF_Comments$month[index]<-month
  DF_Comments$year[index]<-year
  DF_Comments$comment[index]<-txt
  #split link so we can put link in df
  index<-index+1
  closeAllConnections()
}

View(DF_Comments)

showConnections()
closeAllConnections() #close connections

#Don't save as a csv the commas and formatting in raw text will screw it up
save(DF_Comments, file = "DF_Comments.RData")

# Can also write to SQL (this is currently underdeveloped)

require(sqlutils)
require(RSQLite)
require(retention)
library(dplyr)

db <- dbConnect(SQLite(), dbname="DF_Comments.sqlite")
dbWriteTable(conn = db, name = "DF_Comments", value = DF_Comments, row.names = FALSE)

my_db <- src_sqlite(path="DF_Comments.sqlite")
tst<- tbl(my_db, "DF_Comments")
