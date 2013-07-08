makeProfilePlot <- function(mylist,names) 
{
    require(RColorBrewer)
     # find out how many variables we want to include
	numvariables <- length(mylist)
	 # choose ’numvariables’ random colours
	colours <- brewer.pal(numvariables,"Set1")
	 # find out the minimum and maximum values of the variables: 
	mymin <- 1e+20
	mymax <- 1e-20
	for (i in 1:numvariables)
	{
		vectori <- mylist[[i]]
		mini <- min(vectori)
		maxi <- max(vectori)
		if (mini < mymin) { mymin <- mini } 
		if (maxi > mymax) { mymax <- maxi }
	}
	 # plot the variables
	for (i in 1:numvariables) 
	{
		vectori <- mylist[[i]]
		namei <- names[i]
		colouri <- colours[i]
		if (i == 1) { plot(vectori,col=colouri,type="l",ylim=c(mymin,mymax)) } 
		else 		{ points(vectori, col=colouri,type="l") }
		lastxval <- length(vectori)
		lastyval <- vectori[length(vectori)]
		text((lastxval-10),(lastyval),namei,col="black",cex=0.6)
	}
}