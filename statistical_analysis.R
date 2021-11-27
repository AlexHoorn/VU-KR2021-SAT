#### Sudoku SAT Solver
##
## Knowledge Representation
##
## Plots and Statistical Analysis of Experiments 
##
##
## Input: all csv files in Experiments
## Output: -
##
##
## last mod: 24.11.21

# working directory
# setwd("C:/Users/oleh/Documents/Uni/13_Semester/Knowledge_Representation/knowledge-representation-6")

library(ggplot2)


####### Input Data #################

f.names <- dir("experiments/", pattern = ".csv")

bigdat <- NULL

for(i in 1:length(f.names)){
  dat <- read.table(paste("experiments/", f.names[i], sep = ""), header = TRUE, sep = ",")
  dat$i <- f.names[i]
  bigdat <- rbind(bigdat, dat)
}

dat <- bigdat
rm(bigdat)

dat$size <- as.numeric(substr(dat$i, 0, 1))

dat$heuristic <- ifelse(grepl("random", dat$i, fixed = TRUE), "random", ifelse(grepl("dlis", dat$i, fixed = TRUE), "dlis", 
                          ifelse(grepl("dlcs", dat$i, fixed = TRUE), "dlcs", ifelse(grepl("jw_", dat$i, fixed = TRUE), "jw_one", 
                                  ifelse(grepl("jwtwo", dat$i, fixed = TRUE), "jw_two", ifelse(grepl("weighted", dat$i, fixed = TRUE), "weighted", "0"))))))

## TO DO:
# need to add new heuristic names, depending on the names alex gives them


dat$rated <- ifelse(grepl("Rated", dat$i, fixed = TRUE), 1, 0)


####### Hypothesis 1 #################


### violin plots

# 4x4 Sudokus

# duration
violin_4 <- ggplot(dat[dat$size == 4 & dat$rated == 0,], aes(x = heuristic, y = duration)) + geom_violin()
violin_4 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red")

# backtracks
violin_4 <- ggplot(dat[dat$size == 4 & dat$rated == 0,], aes(x = heuristic, y = backtracks)) + geom_violin()
violin_4 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red")


# 9x9 Sudokus

# duration
violin_9 <- ggplot(dat[dat$size == 9 & dat$rated == 0,], aes(x = heuristic, y = duration)) + geom_violin()
violin_9 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red")

# backtracks
violin_9 <- ggplot(dat[dat$size == 9 & dat$rated == 0,], aes(x = heuristic, y = backtracks)) + geom_violin()
violin_9 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red")



### Statistical Analysis




se <- function(x){
  sd(x) / sqrt(length(x))
}


# 4x4
aov4 <- aov(duration ~ heuristic, data = dat[dat$size == 4, ])
summary(aov4)

# post hoc tests
TukeyHSD(aov4)
# descriptive statistics
desc_4 <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = mean)
desc_4$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = se)[,2]

# 9x9
aov9 <- aov(duration ~ heuristic, data = dat[dat$size == 9, ])
summary(aov9)

# post hoc tests
TukeyHSD(aov9)
# descriptive statistics
desc_9 <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = mean)
desc_9$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = se)[,2]




### Scatterplot duration ~ backtracks

heu <- unique(dat$heuristic)
cols <- c("red", "blue", "green", "black", "grey", "yellow", "orange")


plot(duration ~ backtracks, data = dat[dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(0, 6000), ylim = c(0, 100))
abline(lm(duration ~ backtracks, data = dat[dat$heuristic == heu[1],]), col = cols[1])

points(duration ~ backtracks, data = dat[dat$heuristic == heu[2],], col = cols[2])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[3],], col = cols[3])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[4],], col = cols[4])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[5],], col = cols[5])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[6],], col = cols[6])

for(i in 2:length(heu)){
  abline(lm(duration ~ backtracks, data = dat[dat$heuristic == heu[i],]), col = cols[i])
}

# Legend need


## Significance tests for correlation

cor.test(dat[dat$heuristic == heu[1], "duration"], dat[dat$heuristic == heu[1], "backtracks"])
# dlcs: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[2], "duration"], dat[dat$heuristic == heu[2], "backtracks"])
# dlis: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[3], "duration"], dat[dat$heuristic == heu[3], "backtracks"])
# dlis: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[4], "duration"], dat[dat$heuristic == heu[4], "backtracks"])
# jw_one: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[5], "duration"], dat[dat$heuristic == heu[5], "backtracks"])
# jw_two: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[6], "duration"], dat[dat$heuristic == heu[6], "backtracks"])
# random: p < .001, cor = ...

cor.test(dat[dat$heuristic == heu[7], "duration"], dat[dat$heuristic == heu[7], "backtracks"])
# weighted: p < .001, cor = ...




####### Hypothesis 2 #################


