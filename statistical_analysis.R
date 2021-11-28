#### Sudoku SAT Solver
##
## Knowledge Representation
##
## Plots and Statistical Analysis of Experiments 
##
##
## Input: all csv files in Experiments
## Output: "Violin_4.pdf", "Violin_9.pdf", "Violin_16.pdf", 
##         "Scatterplot_all.pdf", "Scatterplot_4.pdf", "Scatterplot_9.pdf",
##         "Scatterplot_16.pdf", "Means.pdf"
##
##
## last mod: 24.11.21

# working directory
# setwd("C:/Users/oleh/Documents/Uni/13_Semester/Knowledge_Representation/knowledge-representation-6")

library(ggplot2)
library(xtable)
library(lattice)


####### Input Data #################

f.names <- dir("experiments/", pattern = ".csv")

bigdat <- NULL

for(i in 1:length(f.names)){
  dat <- read.table(paste("experiments/", f.names[i], sep = ""), header = TRUE, sep = ",")
  dat$i <- f.names[i]
  bigdat <- rbind(bigdat, dat)
}

dat <- bigdat


dat$size <- as.numeric(substr(dat$i, 0, 1))

dat$heuristic <- ifelse(grepl("random", dat$i, fixed = TRUE), "random", ifelse(grepl("dlis", dat$i, fixed = TRUE), "dlis", 
                          ifelse(grepl("dlcs", dat$i, fixed = TRUE), "dlcs", ifelse(grepl("jw_", dat$i, fixed = TRUE), "jw_one", 
                                  ifelse(grepl("jwtwo", dat$i, fixed = TRUE), "jw_two", ifelse(grepl("weighted", dat$i, fixed = TRUE), "weighted",
                                          ifelse(grepl("mams", dat$i, fixed = TRUE), "mams", "moms")))))))


dat$rated <- ifelse(grepl("Rated", dat$i, fixed = TRUE), "yes", "no")

# factorising
dat$rated <- as.factor(dat$rated)
dat$size <- factor(dat$size, levels = c("4","9","1"), labels = c("4", "9", "16"))
dat$heuristic <- as.factor(dat$heuristic)


dat_split <- split(dat, dat$rated)


# remaining:
# dat for all heuristic hypothesis
# dat_cog for the cognitive comparison

dat_cog <- drop(dat_split$yes)
dat <- drop(dat_split$no)

rm(bigdat, f.names, i, dat_split)



####### Hypothesis 1 #################


### violin plots

# 4x4 Sudokus

pdf("Plots/Violin_4.pdf", height = 6, width = 12, pointsize =12)
violin_4 <- ggplot(dat[dat$size == 4,], aes(x = heuristic, y = duration)) + 
  geom_violin() + theme_classic()

violin_4 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red") + 
  stat_summary(fun = median, geom = "point", size = 1, shape = 1, color = "blue") + 
  labs(x = "Heuristics",y = expression("Duration (sec)"),colour = "") + 
  geom_hline(yintercept = 0,linetype = "dashed", color = "grey")

dev.off()


# 9x9 Sudokus

pdf("Plots/Violin_9.pdf", height = 6, width = 12, pointsize =12)
violin_9 <- ggplot(dat[dat$size == 9,], aes(x = heuristic, y = duration)) + 
              geom_violin() + theme_classic()
      
violin_9 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red") + 
  stat_summary(fun = median, geom = "point", size = 1, shape = 1, color = "blue") + 
  labs(x = "Heuristics",y = expression("Duration (sec)"),colour = "") + 
  geom_hline(yintercept = 0,linetype = "dashed", color = "grey")

dev.off()



# 16x16 Sudokus

pdf("Plots/Violin_16.pdf", height = 6, width = 12, pointsize =12)
violin_16 <- ggplot(dat[dat$size == 16,], aes(x = heuristic, y = duration)) +
  geom_violin() + theme_classic()

violin_16 + stat_summary(fun = mean, geom = "point", size = 1, shape = 1, color = "red") +
  stat_summary(fun = median, geom = "point", size = 1, shape = 1, color = "blue") +
  labs(x = "Heuristics",y = expression("Duration (sec)"),colour = "") +
  geom_hline(yintercept = 0,linetype = "dashed", color = "grey")

dev.off()

# sad because of less runs for 16x16




### Statistical Analysis




se <- function(x){
  sd(x) / sqrt(length(x))
}


# 4x4
aov4 <- aov(duration ~ heuristic, data = dat[dat$size == 4, ])
summary(aov4)

# post hoc tests, for the appendix
xtable(TukeyHSD(aov4)$heuristic)

# descriptive statistics, for the report
desc_4 <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = mean)
desc_4$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = se)[,2]



# 9x9
aov9 <- aov(duration ~ heuristic, data = dat[dat$size == 9, ])
summary(aov9)

# post hoc tests, for the appendix
xtable(TukeyHSD(aov9)$heuristic)

# descriptive statistics, for the report
desc_9 <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = mean)
desc_9$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = se)[,2]



# 16x16
aov16 <- aov(duration ~ heuristic, data = dat[dat$size == 16, ])
summary(aov16)

# post hoc tests, for the appendix
xtable(TukeyHSD(aov16)$heuristic)

# descriptive statistics, for the report
desc_16 <- aggregate(duration ~ heuristic, data = dat[dat$size == 16, ], FUN = mean)
desc_16$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 16, ], FUN = se)[,2]




### Scatterplot duration ~ backtracks

heu <- unique(dat$heuristic)
cols <- c("firebrick1", "darkorange1", "black", "grey", "darkgreen", "darkblue", "darkviolet", "lightsalmon4")




pdf("Plots/Scatterplot_all.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ backtracks, data = dat[dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(0, 18000), ylim = c(0, 600), xlab = "Number of backtracks", ylab = "Duration (sec)")
abline(lm(duration ~ backtracks, data = dat[dat$heuristic == heu[1],]), col = cols[1])

legend("bottomright", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

points(duration ~ backtracks, data = dat[dat$heuristic == heu[2],], col = cols[2])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[3],], col = cols[3])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[4],], col = cols[4])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[5],], col = cols[5])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[6],], col = cols[6])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[7],], col = cols[7])
points(duration ~ backtracks, data = dat[dat$heuristic == heu[8],], col = cols[8])

for(i in 2:length(heu)){
  abline(lm(duration ~ backtracks, data = dat[dat$heuristic == heu[i],]), col = cols[i])
}

#abline(h = 0, lty = "dotdash", col = "darkgrey")
abline(v = 0, lty = "dotdash", col = "darkgrey")

# abline until legend
segments(0, 0, 13500, 0, lty = "dotdash", col = "darkgrey")

box()

dev.off()



#### Maybe for all 3 sizes?

# 4x4
help_dat <- dat[dat$size == 4,]

pdf("Plots/Scatterplot_4.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(0, 5), ylim = c(0, 0.025), xlab = "Number of backtracks", ylab = "Duration (sec)")
abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],]), col = cols[1])

legend("topleft", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[2],], col = cols[2])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[3],], col = cols[3])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[4],], col = cols[4])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[5],], col = cols[5])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[6],], col = cols[6])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[7],], col = cols[7])
points(duration ~ jitter(backtracks, factor = 0.5), data = help_dat[help_dat$heuristic == heu[8],], col = cols[8])

# coordinates
abline(h = 0, lty = "dotdash", col = "darkgrey")
#abline(v = 0, lty = "dotdash", col = "darkgrey")

# abline until legend
segments(0, 0, 0, 0.016, lty = "dotdash", col = "darkgrey")

for(i in 2:length(heu)){
  if(i != 6){
    abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[i],]), col = cols[i])
  }
}

#moms zero backtracks
segments(0, 0, 0, 0.016, lty = "solid", col = cols[6])

box()

dev.off()


# 9x9
help_dat <- dat[dat$size == 9,]

pdf("Plots/Scatterplot_9.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(0, 6000), ylim = c(0, 45), xlab = "Number of backtracks", ylab = "Duration (sec)")
abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],]), col = cols[1])

legend("topleft", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[2],], col = cols[2])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[3],], col = cols[3])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[4],], col = cols[4])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[5],], col = cols[5])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[6],], col = cols[6])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[7],], col = cols[7])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[8],], col = cols[8])

# coordinates
abline(h = 0, lty = "dotdash", col = "darkgrey")
#abline(v = 0, lty = "dotdash", col = "darkgrey")

# abline until legend
segments(0, 0, 0, 30, lty = "dotdash", col = "darkgrey")

for(i in 2:length(heu)){
  abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[i],]), col = cols[i])
}


box()

dev.off()



# 16x16
help_dat <- dat[dat$size == 16,]

pdf("Plots/Scatterplot_16.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(50, 30500), ylim = c(0, 600), xlab = "Number of backtracks", ylab = "Duration (sec)")
abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],]), col = cols[1])

legend("bottomright", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[2],], col = cols[2])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[3],], col = cols[3])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[4],], col = cols[4])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[5],], col = cols[5])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[6],], col = cols[6])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[7],], col = cols[7])
points(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[8],], col = cols[8])

# coordinates
#abline(h = 0, lty = "dotdash", col = "darkgrey")
abline(v = 0, lty = "dotdash", col = "darkgrey")

# abline until legend
segments(0, 0, 25000, 0, lty = "dotdash", col = "darkgrey")

for(i in 2:length(heu)){
  abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[i],]), col = cols[i])
}

box()

dev.off()



## Significance tests for correlation

cor.test(dat[dat$heuristic == heu[1], "duration"], dat[dat$heuristic == heu[1], "backtracks"])
# dlcs: p < .001, cor = .89; dlcs

cor.test(dat[dat$heuristic == heu[2], "duration"], dat[dat$heuristic == heu[2], "backtracks"])
# dlis: p < .001, cor = .92; dlis

cor.test(dat[dat$heuristic == heu[3], "duration"], dat[dat$heuristic == heu[3], "backtracks"])
# dlis: p < .001, cor = .76; jw_one

cor.test(dat[dat$heuristic == heu[4], "duration"], dat[dat$heuristic == heu[4], "backtracks"])
# jw_one: p < .001, cor = .59; jw_two

cor.test(dat[dat$heuristic == heu[5], "duration"], dat[dat$heuristic == heu[5], "backtracks"])
# jw_two: p < .001, cor = .63; mams

cor.test(dat[dat$heuristic == heu[6], "duration"], dat[dat$heuristic == heu[6], "backtracks"])
# random: p < .001, cor = .78; moms

cor.test(dat[dat$heuristic == heu[7], "duration"], dat[dat$heuristic == heu[7], "backtracks"])
# weighted: p < .001, cor = .83; random

cor.test(dat[dat$heuristic == heu[8], "duration"], dat[dat$heuristic == heu[8], "backtracks"])
# weighted: p < .001, cor = .94; weighted



####### Hypothesis 2 #################

desc <- aggregate(duration ~ heuristic + size, data = dat, FUN = mean)
desc$se <- aggregate(duration ~ heuristic + size, data = dat, FUN = se)[,3]
desc <- desc[order(desc$heuristic), ]

## Plot

pdf("Plots/Means.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[1],], col = cols[1], type = "b",
     ylim = c(0, 420), axes = FALSE, xlab = "Size", ylab = "Mean duration (sec)")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[2],], col = cols[2], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[3],], col = cols[3], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[4],], col = cols[4], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[5],], col = cols[5], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[6],], col = cols[6], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[7],], col = cols[7], type = "b")
points(duration ~ as.numeric(size), data = desc[desc$heuristic == heu[8],], col = cols[8], type = "b")

legend("topleft", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

axis(2)
axis(1, at = c(1,2,3), labels = c("4x4", "9x9", "16x16"))

arrows(1:3, desc$duration - desc$se,
       1:3, desc$duration + desc$se,
       length = .01, code = 3, angle = 90, lwd = 1.5, col = rep(cols, each = 3))

box()

dev.off


## Statistical Analysis

dat$size <- as.numeric(as.character(dat$size))
dat <- dat[order(dat$size), ]

m1 <- lm(duration ~  size, data = dat)
m2 <- lm(duration ~  size * I(size^2), data = dat)
m3 <- lm(duration ~ heuristic + size * I(size^2), data = dat)
m4 <- lm(duration ~ heuristic * size * I(size^2), data = dat)


# Likelihood-Ratio Test
anova(m1,m2, m3, m4)
# X^2(1) = 3227.27, p < .001; its quadratic
# X^2(7) = 6.92, p < .001; different intercepts per heuristic
# X^2(14) = 33.18, p < .001; different linear and quadratic slops per heuristic


# Visualization
xyplot(duration + predict(m1) + predict(m2) + predict(m3) ~ size | heuristic, dat, type=c("p", "l", "l", "l"),
       pch=16, strip = strip.custom(bg="gray96"), grid=TRUE,
       distribute.type = TRUE, par.strip.text=list(cex=.8),
       layout=c(8,1), ylab="Duration (sec)", xlab="Size")




####### Hypothesis 3 #################



dat_cog$identifier <- as.factor(dat_cog$identifier)
desc <- aggregate(duration ~ identifier + heuristic, data = dat_cog, FUN = mean)


pdf("Plots/Means_Cog.pdf", width = 6, height = 6, pointsize = 10)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[1],], col = cols[1], type = "b",
     ylim = c(0, 12), axes = FALSE, xlab = "Difficulty of Sudokus", ylab = "Mean duration (sec)")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[2],], col = cols[2], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[3],], col = cols[3], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[4],], col = cols[4], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[5],], col = cols[5], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[6],], col = cols[6], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[7],], col = cols[7], type = "b")
points(duration ~ as.numeric(identifier), data = desc[desc$heuristic == heu[8],], col = cols[8], type = "b")

legend("topleft", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

axis(2)
axis(1, at = c(1:10), labels = levels(dat_cog$identifier))

box()

dev.off()


# analysis

cor.test(dat_cog$duration, dat_cog$identifier)
# r = 0.05, p = .068, no significant (linear) correlation between difficulty and mean duration

