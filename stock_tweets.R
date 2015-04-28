


stock.google <- read.table(file="~/Dropbox/tweets/appel_stock.csv",sep=",")

stock.dates <- as.character(stock.google$V1[3:length(stock.google$V1)]) ### deleting first two rows
stock.dates.consec <- as.character(stock.google$V1[3:length(stock.google$V1)])
stock.high <- as.numeric(as.character(stock.google$V5[3:length(stock.google$V5)]))
stock.low <- as.numeric(as.character(stock.google$V6[3:length(stock.google$V6)]))
stock.open <- as.numeric(as.character(stock.google$V5[3:length(stock.google$V4)]))
stock.close <- as.numeric(as.character(stock.google$V6[3:length(stock.google$V2)]))



one.day <- function(date1,date2) {

  daysPerMonth <- c(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
       
      month1 <- as.numeric(date1[2])
      day1<- as.numeric(date1[3])

      month2 <- as.numeric(date2[2])
 	day2 <- as.numeric(date2[3])

	if (abs(month2 - month1) > 1){
		return (0)
        }

	if(month1 == month2){
		if(abs(day2-day1) > 1){
			return (0)
              }
		else{
			return (1)
             }
       }
	lastDayMonth1 = daysPerMonth[month1]
	lastDayMonth2 = daysPerMonth[month2]

	if(day1 == lastDayMonth1 && day2 == 1){
		return (1)
         }
	if(day2 == lastDayMonth2 && day1 == 1){
		return (1)
        }

	return (0)


}


month.day <- strsplit(stock.dates,"/")


consec.dates <- list() ######## now grab the entries of stock.dates that are a day apart


for(x in 2:length(month.day)){

    if(one.day(month.day[[x-1]],month.day[[x]])) {

   d1 <- paste(month.day[[x-1]][1],month.day[[x-1]][2],month.day[[x-1]][3],sep="/")

  d2 <- paste(month.day[[x]][1],month.day[[x]][2],month.day[[x]][3],sep="/")

        consec.dates[[length(consec.dates)+1]] <- c(d1,d2)          
   }    

}


google.data <- read.table(file="~/Dropbox/tweets/FinalResults/apple.csv", sep=",", fill=TRUE,na.string="")
 
 print("here")
class <- google.data$V2[!is.na(google.data$V2)]
retweets <- google.data$V4[!is.na(google.data$V4)]
date.tweet <- google.data$V5[!is.na(google.data$V5)]
followers <- google.data$V6[!is.na(google.data$V6)]
friends <- google.data$V7[!is.na(google.data$V7)]


dates <- strsplit(as.character(date.tweet)," ")


for (x in 1:length(dates)) {

    dates[x] <- paste(dates[x][[1]][3], dates[x][[1]][4],sep=" ")
}


dates <- unique(unlist(dates)) #### contains list of distinct dates in the twitter data

dates <- dates[which(dates != "Mar 3")] ####### fix this for real

dates <- dates[order(dates)]



   ########### now delete all the entries of consec.dates that we don't have twitter data on the first day for ###############3

    ######## step 1, make "dates" readable by consec.dates 

months <- vector(mode="list",length=12)
names(months) <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")



months[["Jan"]] <- paste("0","1",sep="")
months[["Feb"]] <- paste("0","2",sep="")
months[["Mar"]] <- paste("0","3",sep="")
months[["Apr"]] <- paste("0","4",sep="")
months[["May"]] <- paste("0","5",sep="")
months[["Jun"]] <- paste("0","6",sep="")
months[["Jul"]] <- paste("0","7",sep="")
months[["Aug"]] <- paste("0","8",sep="")
months[["Sep"]] <- paste("0","9",sep="")
months[["Oct"]] <- as.character(10)
months[["Nov"]] <- as.character(11)
months[["Dec"]] <- as.character(12)




f <- function(s) s[[1]][1]
first.days <- sapply(consec.dates,f)

dates.new <- vector(length=length(dates)) ##### readable by stock.dates and consec.dates

for ( x in 1:length(dates)){
  
  m <- unlist(strsplit(dates[x]," "))

  dates.new[x] <- paste("2015/",months[[m[1]]],"/", m[2],sep="" )

}


index.dates <- vector(mode="list")

 for (x in 1:length(first.days)) {
                                                                                                                                               

     if (length(which( dates.new == first.days[x] ) ) != 0) {  ##### if  we have twitter data for that day 
     
     index.dates[[length(index.dates)+1]] <- c( which( stock.dates == first.days[x] ), which(stock.dates == consec.dates[[ x]][2] ) )##### indices of stock.dates that we're interested in ( for high/low values)

      }

      else {

            consec.dates[[ x ]] <- NA   ##### get rid of the entries of consec.dates that don't have twitter data
      }
     
}


consec.dates <- consec.dates[which(!is.na(consec.dates))]

fd.final <- sapply(consec.dates,f)   ##### convert fd.final back into from readable by date.tweet



months.rev <- vector(mode="list",length=12)

#names(months) <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

months.rev[["01"]] <- "Jan"
months.rev[["02"]] <- "Feb"
months.rev[["03"]] <- "Mar"
months.rev[["04"]] <- "Apr"
months.rev[["05"]] <- "May"
months.rev[["06"]] <- "Jun"
months.rev[["07"]] <- "Jul"
months.rev[["08"]] <- "Aug"
months.rev[["09"]] <- "Sep"
months.rev[["10"]] <- "Oct"
months.rev[["11"]] <- "Nov"
months.rev[["12"]] <- "Dec"

fdt.final <- vector(length=length(fd.final))


for (x in 1:length(fd.final)){

   tmp <- unlist(strsplit(fd.final[x],"/"))
   fdt.final[x] <- paste( months.rev[[ tmp[2] ]] , tmp[3],sep=" " )


}

tweets.perDay <- vector()
num.pos <- vector()

for (k in seq(length(fdt.final))){


	tweets.perDay[k] <- length(grep(fdt.final[k],date.tweet))

    num.pos[k] <- length(which(class[grepl(fdt.final[k],date.tweet)] == " neg" ))

}


percent.pos <- num.pos/tweets.perDay


############# now get open and close values ##############


open <- vector(mode="list")
close <- vector(mode="list")

for ( x in 1:length(index.dates)){

     open[[x]] <- c(stock.open[index.dates[[x]] [1] ], stock.open[ index.dates[[x]] [2] ] )  
     close[[x]] <- c(stock.close[index.dates[[x]] [1] ], stock.close[ index.dates[[x]] [2] ] )             

}


 open.vec <- vector()

 close.vec <- vector()
       

     for( x in 1:length(open)) {
       
        open.vec[x] <- (open[[x]][2] - open[[x]][1]) 
        close.vec[x] <- (close[[x]][2] - close[[x]][1]) 


      }