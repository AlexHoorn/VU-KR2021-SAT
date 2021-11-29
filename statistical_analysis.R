#### Sudoku SAT Solver
##
## Knowledge Representation
##
## Plots and Statistical Analysis of Experiments 
##
##
## Input: all *.csv and *.txt files in Experiments
## Output: "Violin_4.pdf", "Violin_9.pdf", "Violin_16.pdf", 
##         "Scatterplot_all.pdf", "Scatterplot_4.pdf", "Scatterplot_9.pdf",
##         "Scatterplot_16.pdf", "Means.pdf", "Means_cog.pdf"
##
##
## last mod: 27.11.21

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
TukeyHSD(aov4)$heuristic
# diff           lwr           upr        p adj
# dlis-dlcs       -0.0009607196 -1.598982e-03 -3.224575e-04 1.492716e-04
# jw_one-dlcs     -0.0006233048 -1.261567e-03  1.495726e-05 6.127955e-02
# jw_two-dlcs     -0.0002549744 -8.932365e-04  3.832877e-04 9.278047e-01
# mams-dlcs        0.0056256008  4.987339e-03  6.263863e-03 0.000000e+00
# moms-dlcs        0.0019889665  1.350704e-03  2.627229e-03 0.000000e+00
# random-dlcs      0.0008426762  2.044141e-04  1.480938e-03 1.685757e-03
# weighted-dlcs   -0.0003935981 -1.031860e-03  2.446640e-04 5.692370e-01
# jw_one-dlis      0.0003374147 -3.008474e-04  9.756769e-04 7.463957e-01
# jw_two-dlis      0.0007057452  6.748311e-05  1.344007e-03 1.844928e-02
# mams-dlis        0.0065863204  5.948058e-03  7.224583e-03 0.000000e+00
# moms-dlis        0.0029496861  2.311424e-03  3.587948e-03 0.000000e+00
# random-dlis      0.0018033957  1.165134e-03  2.441658e-03 0.000000e+00
# weighted-dlis    0.0005671215 -7.114060e-05  1.205384e-03 1.239214e-01
# jw_two-jw_one    0.0003683305 -2.699316e-04  1.006593e-03 6.516479e-01
# mams-jw_one      0.0062489057  5.610644e-03  6.887168e-03 0.000000e+00
# moms-jw_one      0.0026122713  1.974009e-03  3.250533e-03 0.000000e+00
# random-jw_one    0.0014659810  8.277189e-04  2.104243e-03 0.000000e+00
# weighted-jw_one  0.0002297068 -4.085553e-04  8.679689e-04 9.581216e-01
# mams-jw_two      0.0058805752  5.242313e-03  6.518837e-03 0.000000e+00
# moms-jw_two      0.0022439408  1.605679e-03  2.882203e-03 0.000000e+00
# random-jw_two    0.0010976505  4.593884e-04  1.735913e-03 6.107108e-06
# weighted-jw_two -0.0001386237 -7.768858e-04  4.996384e-04 9.979289e-01
# moms-mams       -0.0036366343 -4.274896e-03 -2.998372e-03 0.000000e+00
# random-mams     -0.0047829247 -5.421187e-03 -4.144663e-03 0.000000e+00
# weighted-mams   -0.0060191989 -6.657461e-03 -5.380937e-03 0.000000e+00
# random-moms     -0.0011462903 -1.784552e-03 -5.080282e-04 1.781685e-06
# weighted-moms   -0.0023825645 -3.020827e-03 -1.744302e-03 0.000000e+00
# weighted-random -0.0012362742 -1.874536e-03 -5.980121e-04 1.551330e-07

# descriptive statistics, for the report
desc_4 <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = mean)
desc_4$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 4, ], FUN = se)[,2]



# 9x9
aov9 <- aov(duration ~ heuristic, data = dat[dat$size == 9, ])
summary(aov9)

# post hoc tests, for the appendix
TukeyHSD(aov9)$heuristic
# diff         lwr         upr        p adj
# dlis-dlcs       -0.7386063 -2.54554753  1.06833503 9.190120e-01
# jw_one-dlcs     -0.5032447 -2.31018599  1.30369657 9.903169e-01
# jw_two-dlcs     -0.3228834 -2.12982468  1.48405788 9.994153e-01
# mams-dlcs        1.5325720 -0.27436927  3.33951329 1.656493e-01
# moms-dlcs       -1.1165508 -2.92349208  0.69039047 5.666036e-01
# random-dlcs     -1.2681901 -3.07513134  0.53875121 3.945195e-01
# weighted-dlcs   -1.8580168 -3.66495804 -0.05107548 3.878473e-02
# jw_one-dlis      0.2353615 -1.57157974  2.04230282 9.999293e-01
# jw_two-dlis      0.4157228 -1.39121843  2.22266413 9.970153e-01
# mams-dlis        2.2711783  0.46423698  4.07811954 3.588170e-03
# moms-dlis       -0.3779446 -2.18488583  1.42899672 9.983724e-01
# random-dlis     -0.5295838 -2.33652509  1.27735746 9.868847e-01
# weighted-dlis   -1.1194105 -2.92635179  0.68753077 5.632731e-01
# jw_two-jw_one    0.1803613 -1.62657997  1.98730259 9.999885e-01
# mams-jw_one      2.0358167  0.22887545  3.84275800 1.492077e-02
# moms-jw_one     -0.6133061 -2.42024737  1.19363519 9.695958e-01
# random-jw_one   -0.7649454 -2.57188663  1.04199593 9.038415e-01
# weighted-jw_one -1.3547720 -3.16171332  0.45216923 3.067559e-01
# mams-jw_two      1.8554554  0.04851414  3.66239669 3.929063e-02
# moms-jw_two     -0.7936674 -2.60060868  1.01327388 8.853860e-01
# random-jw_two   -0.9453067 -2.75224794  0.86163461 7.564574e-01
# weighted-jw_two -1.5351334 -3.34207463  0.27180792 1.640293e-01
# moms-mams       -2.6491228 -4.45606409 -0.84218154 2.559569e-04
# random-mams     -2.8007621 -4.60770335 -0.99382080 7.917812e-05
# weighted-mams   -3.3905888 -5.19753005 -1.58364749 4.566602e-07
# random-moms     -0.1516393 -1.95858054  1.65530202 9.999965e-01
# weighted-moms   -0.7414660 -2.54840723  1.06547532 9.174455e-01
# weighted-random -0.5898267 -2.39676797  1.21711458 9.755642e-01


# descriptive statistics, for the report
desc_9 <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = mean)
desc_9$se <- aggregate(duration ~ heuristic, data = dat[dat$size == 9, ], FUN = se)[,2]



# 16x16
aov16 <- aov(duration ~ heuristic, data = dat[dat$size == 16, ])
summary(aov16)

# post hoc tests, for the appendix
TukeyHSD(aov16)$heuristic
# diff        lwr        upr        p adj
# dlis-dlcs         -5.571552 -187.04273 175.899630 1.000000e+00
# jw_one-dlcs       40.129122 -135.57959 215.837838 9.965514e-01
# jw_two-dlcs       11.067454 -164.64126 186.776170 9.999994e-01
# mams-dlcs        227.177020   77.06947 377.284572 2.444220e-04
# moms-dlcs         67.707246  -83.51874 218.933231 8.599376e-01
# random-dlcs      107.847077  -47.55556 263.249713 3.897620e-01
# weighted-dlcs     21.669431 -130.79686 174.135720 9.998424e-01
# jw_one-dlis       45.700674 -130.00804 221.409390 9.923342e-01
# jw_two-dlis       16.639006 -159.06971 192.347722 9.999900e-01
# mams-dlis        232.748571   82.64102 382.856124 1.561217e-04
# moms-dlis         73.278798  -77.94719 224.504783 8.036964e-01
# random-dlis      113.418629  -41.98401 268.821265 3.246040e-01
# weighted-dlis     27.240983 -125.22531 179.707272 9.992832e-01
# jw_two-jw_one    -29.061668 -198.81241 140.689079 9.994580e-01
# mams-jw_one      187.047898   43.96037 330.135425 2.573375e-03
# moms-jw_one       27.578124 -116.68227 171.838520 9.988876e-01
# random-jw_one     67.717955  -80.91496 216.350867 8.487441e-01
# weighted-jw_one  -18.459691 -164.01976 127.100374 9.999268e-01
# mams-jw_two      216.109565   73.02204 359.197092 2.536585e-04
# moms-jw_two       56.639792  -87.62060 200.900187 9.245061e-01
# random-jw_two     96.779623  -51.85329 245.412534 4.743328e-01
# weighted-jw_two   10.601977 -134.95809 156.162041 9.999984e-01
# moms-mams       -159.469773 -271.13797 -47.801578 6.670293e-04
# random-mams     -119.329942 -236.59233  -2.067559 4.308284e-02
# weighted-mams   -205.507589 -318.84980 -92.165378 5.506470e-06
# random-moms       40.139831  -78.55089 158.830554 9.652655e-01
# weighted-moms    -46.037815 -160.85714  68.781512 9.162895e-01
# weighted-random  -86.177646 -206.44468  34.089384 3.480477e-01

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
segments(-1000, 0, 13500, 0, lty = "dotdash", col = "darkgrey")

legend("bottomright", legend = heu, col = cols, 
       lty = 1, cex=1, lwd = 2, box.col = "white")

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
segments(0, -1, 0, 0.016, lty = "dotdash", col = "darkgrey")

for(i in 2:length(heu)){
  if(i != 6){
    abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[i],]), col = cols[i])
  }
}

#moms zero backtracks
segments(0, -1, 0, 0.016, lty = "solid", col = cols[6])

box()

dev.off()


# 9x9
help_dat <- dat[dat$size == 9,]

pdf("Plots/Scatterplot_9.pdf", width = 6, height = 6, pointsize = 12)
par(mgp = c(2.5, 0.7, 0), mar = c(4, 4, 1, 1) + 0.1)

plot(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[1],], type = "p", col = cols[1], 
     xlim = c(0, 13500), ylim = c(0, 45), xlab = "Number of backtracks", ylab = "Duration (sec)")
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
segments(0, -10, 0, 30, lty = "dotdash", col = "darkgrey")

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
segments(-5000, 0, 23000, 0, lty = "dotdash", col = "darkgrey")

for(i in 2:length(heu)){
  abline(lm(duration ~ backtracks, data = help_dat[help_dat$heuristic == heu[i],]), col = cols[i])
}

box()

dev.off()



## Significance tests for correlation

cor.test(dat[dat$heuristic == heu[1], "duration"], dat[dat$heuristic == heu[1], "backtracks"])
# dlcs: p = .002, cor = .22;

cor.test(dat[dat$heuristic == heu[2], "duration"], dat[dat$heuristic == heu[2], "backtracks"])
# dlis: p = .107, cor = .114;

cor.test(dat[dat$heuristic == heu[3], "duration"], dat[dat$heuristic == heu[3], "backtracks"])
# dlis: p < .001, cor = .76;

cor.test(dat[dat$heuristic == heu[4], "duration"], dat[dat$heuristic == heu[4], "backtracks"])
# jw_one: p < .001, cor = .59;

cor.test(dat[dat$heuristic == heu[5], "duration"], dat[dat$heuristic == heu[5], "backtracks"])
# jw_two: p < .001, cor = .63;

cor.test(dat[dat$heuristic == heu[6], "duration"], dat[dat$heuristic == heu[6], "backtracks"])
# random: p < .001, cor = .78;

cor.test(dat[dat$heuristic == heu[7], "duration"], dat[dat$heuristic == heu[7], "backtracks"])
# random: p < .001, cor = .83;

cor.test(dat[dat$heuristic == heu[8], "duration"], dat[dat$heuristic == heu[8], "backtracks"])
# weighted: p < .001, cor = .94;



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

dev.off()


## Statistical Analysis

dat$size <- as.numeric(as.character(dat$size))
dat <- dat[order(dat$size), ]

m1 <- lm(duration ~  size, data = dat)
m2 <- lm(duration ~  size * I(size^2), data = dat)
m3 <- lm(duration ~ heuristic + size * I(size^2), data = dat)
m4 <- lm(duration ~ heuristic * size * I(size^2), data = dat)


# Likelihood-Ratio Test
anova(m1,m2, m3, m4)
# X^2(1) = 4645.75, p < .001; its quadratic
# X^2(7) = 11.50, p < .001; different intercepts per heuristic
# X^2(14) = 62.69, p < .001; different linear and quadratic slops per heuristic


# Visualization
xyplot(duration + predict(m4) ~ size | heuristic, dat, type=c("p", "l"),
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
dat_cog$identifier <- as.numeric(as.character(dat_cog$identifier))
cor.test(dat_cog$duration, dat_cog$identifier)
# r = 0.04, p = .115, no significant (linear) correlation between difficulty and mean duration



## timeouts:

# order as levels(dat$heuristic)
timeouts <- c(25, 25, 24, 24, 13, 14, 17, 15)

n <- 32

pct <- timeouts/n

round(pct, 2)
# dlcs     dlis     jw_one   jw_two   mams     moms     random   weighted
# 0.78     0.78       0.75     0.75   0.41     0.44       0.53       0.47



# end