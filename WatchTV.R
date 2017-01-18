library(digest)
library(jsonlite)

autocomplete_key <- "twf3ry66pb7stjdjuzzhzwdv"
autocomplete_secret_key <- "TeaCG2TbdN"
search_key <- "jh6b4hqegxr2bwq97kwf7w3s"
search_secret_key <- "f3G8TBfxgk"
tvlistings_key <- "ytbfb5tufg5hdhyratpc6ryr"
line <- paste(search_key,search_secret_key,str(as.integer(as.POSIXct(Sys.time()))))
#line <- line.encode('utf-8')
sig <- digest(line)

comcast_serviceID <- "61805"
test_serviceID <- "63891"

duration <- 60
startdate <- Sys.time()
startdate <- paste(substr(startdate, 1, 10),"T",substr(startdate, 12, 13),"%3A",substr(startdate, 15, 16),"%3A",substr(startdate, 18, 19),"Z",sep="")

url_services <- paste("http://api.rovicorp.com/TVlistings/v9/listings/services/postalcode/32304/info?locale=en-US&countrycode=US&apikey=",tvlistings_key,"&sig=",sig, sep="")
url_gridschedule <- paste("http://api.rovicorp.com/TVlistings/v9/listings/gridschedule/",test_serviceID,"/info?apikey=",tvlistings_key,"&sig=",sig,"&locale=en-US&duration=",duration,"&startdate=",startdate, sep="")
url_servicedetails <- paste("http://api.rovicorp.com/TVlistings/v9/listings/servicedetails/serviceid/",test_serviceID,"/info?locale=en-US&apikey=",tvlistings_key,"&sig=",sig, sep="")

data <- fromJSON(url_gridschedule)

grid_schedule_results <- data$"GridScheduleResult"
grid_channels <- grid_schedule_results$"GridChannels"

call_letters <- c("ESPN", "ESPN2", "MTV", "VH1", "BET", "TLC", "DISNEY", "CNN", "msnbc", "CNBC", "DSC", "A&E", "FX", "USA", "NBCSN", "COMEDY", "SPK", "TNT", "AMC", "TBS", "Syfy", "truTV", "TOON", "ESPNEWS", "SCI", "BBC")
call_letters2 <- c("A&E", "AMC", "ANIMAL", "BBC", "BET", "CNBC", "CNN", "TOON", "COMEDY", "DSC", "DISNEY", "E!", "FX", "FNC", "msnbc", "MTV", "NIK", "SPK", "TBS", "TNT", "USA")
call_letters2_ID <- c(426, 433, 448, 3389, 439, 28, 429, 3460, 26, 399, 430, 408, 398, 450, 1202, 440, 431, 425, 410, 427, 432)

call_letters_top <- c("WCBS", "WNBC", "WABC", "UNI", "ESPN", "TBS", "USA", "DISNEY", "FNC", "TNT", "DSC", "HIST", "HGTV", "AMC", "TELMUN", "FX", "FOOD", "LIFE", "Syfy", "A&E", "TLC", "HALMRK", "BRAVO", "SPK", "CNN", "ANIMAL", "DISJr", "VH1", "TVLAND", "MTV", "BET", "msnbc", "COMEDY", "E!", "NGC", "OWN", "WE", "truTV", "LMN", "NicJr", "TRAVEL", "GSN", "ESPN2", "FXX", "HMMHD", "FS1", "INSP", "NBCSN", "CNBC", "DISXD", "HLN")
call_letters_top_ID <- c(102, 328, 663, 417, 423, 410, 432, 430, 450, 427, 399, 1254, 424, 433, 1986, 398, 2006, 438, 1232, 426, 452, 1216, 404, 425, 429, 448, 34495, 1275, 1269, 440, 439, 1202, 26, 408, 9426, 28508, 2193, 33, 3818, 4968, 1260, 1184, 435, 44425, 20666, 44423, 1193, 1219, 28, 3474, 428)

#my_channels <- grid_channels[is.element(grid_channels$SourceId, call_letters_top_ID),]
my_channels <- grid_channels[is.element(grid_channels$SourceId, call_letters_top_ID[1]),]
for(i in 2:10) {
  my_channels <- rbind(my_channels, grid_channels[is.element(grid_channels$SourceId, call_letters_top_ID[i]),])
}


file <- file("C:/Users/Ian/Dropbox/WatchTV/testpostText.txt")
text <- "Below are the top 10 most watched networks. If the newtwork name is in blue that means a post for it has already been created and you can click it to go to that discussion. If there is a network name that is not blue and you wish to have a thread for it, please make a comment below with just the network name and it will automatically be created for you.\n\n"
for (i in 1:10) {
  text <- paste(text, "*",my_channels$SourceLongName[i],"\n")
}
writeLines(text,file)
close(file)

airings = my_channels$Airings
for(i in 1:length(airings)) {
  a <- airings[[i]]
  for(num_of_airings in 1:length(a$AiringTime)) {
    date <- substr(a$AiringTime[num_of_airings], 1, 10)
    year <- substr(date,1,4)
    month <- substr(date,6,7)
    day <- substr(date,9,10)
    time <- substr(a$AiringTime[num_of_airings], 12, 19)
    hour <- substr(time, 1, 2)
    min <- substr(time, 4, 5)
    sec <- substr(time, 7, 8)
    file_name <- paste("C:/Users/Ian/Dropbox/WatchTV/Posts/",my_channels$CallLetters[i],"sDATE",date,"eDATE","sTIME",hour,min,sec,"eTIME",".txt", sep="")
    if(!file.exists(file_name)) {
      file2 <- file(file_name)
      text2 <- paste("T-",a$Title[num_of_airings], "\n",sep="")
      text2 <- paste(text2,"This is a post for the network ", my_channels$SourceLongName[i], "\n\n", "Currently airing is ", a$Title[num_of_airings], "\n\n", "Start time is : ",time,"\n\n", "Duration: ",a$Duration[num_of_airings], "\n\n", "Category: ", a$Category[num_of_airings],sep="" )
      
      writeLines(text2,file2)
      close(file2)
    }
  }
}


