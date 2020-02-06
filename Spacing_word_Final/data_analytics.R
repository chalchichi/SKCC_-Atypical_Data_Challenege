install.packages("caret")
install.packages("ggcorrplot")
install.packages("xgboost")
install.packages("caretEnsemble")
install.packages("randomForest")

library(ggcorrplot)
library(caret)
library(caretEnsemble)
library(randomForest)
library(xgboost)

dat=read.csv("word_v3_last.csv")
dat=dat[,-1]
dat=as.matrix(dat)
train=dat[1:1500,]
pred=dat[1501:2000,-dim(train)[2]]
ans=dat[1501:2000,dim(train)[2]]
#grid search
grid_default <- expand.grid(
  nrounds = 100,
  max_depth = 6,
  eta = 0.3,
  gamma = 0,
  colsample_bytree = 1,
  min_child_weight = 1,
  subsample = 1
)

#########################################
nrounds=300
tune_grid <- expand.grid(
  nrounds = seq(from = 200, to = nrounds, by = 50),
  eta = c(0.025, 0.05, 0.1, 0.3),
  max_depth = c(2, 3, 4, 5, 6),
  gamma = 0,
  colsample_bytree = 1,
  min_child_weight = 1,
  subsample = 1
)

train_control <- caret::trainControl(
  method = "none",
  verboseIter = FALSE, # no training log
  allowParallel = TRUE # FALSE for reproducible results 
)
input_x=train[,1:dim(train)[2]-1]
input_y=train[,dim(train)[2]]
xgb_tune <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid,
  method = "xgbTree",
  verbose = TRUE
)
xgb_tune
tuneplot <- function(x, probs = .90) {
  ggplot(x) +
    coord_cartesian(ylim = c(quantile(x$results$RMSE, probs = probs), min(x$results$RMSE))) +
    theme_bw()
}

tuneplot(xgb_tune)


######################################
tune_grid2 <- expand.grid(
  nrounds = seq(from = 50, to = nrounds, by = 50),
  eta = xgb_tune$bestTune$eta,
  max_depth = ifelse(xgb_tune$bestTune$max_depth == 2,
                     c(xgb_tune$bestTune$max_depth:4),
                     xgb_tune$bestTune$max_depth - 1:xgb_tune$bestTune$max_depth + 1),
  gamma = 0,
  colsample_bytree = 1,
  min_child_weight = c(1, 2, 3),
  subsample = 1
)

xgb_tune2 <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid2,
  method = "xgbTree",
  verbose = TRUE
  
)

tuneplot(xgb_tune2)
#############################################

tune_grid3 <- expand.grid(
  nrounds = seq(from = 50, to = nrounds, by = 50),
  eta = xgb_tune$bestTune$eta,
  max_depth = xgb_tune2$bestTune$max_depth,
  gamma = 0,
  colsample_bytree = c(0.4, 0.6, 0.8, 1.0),
  min_child_weight = xgb_tune2$bestTune$min_child_weight,
  subsample = c(0.5, 0.75, 1.0)
)

xgb_tune3 <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid3,
  method = "xgbTree",
  verbose = TRUE
)

tuneplot(xgb_tune3, probs = .95)


###########################################
tune_grid4 <- expand.grid(
  nrounds = seq(from = 50, to = nrounds, by = 50),
  eta = xgb_tune$bestTune$eta,
  max_depth = xgb_tune2$bestTune$max_depth,
  gamma = c(0, 0.05, 0.1, 0.5, 0.7, 0.9, 1.0),
  colsample_bytree = xgb_tune3$bestTune$colsample_bytree,
  min_child_weight = xgb_tune2$bestTune$min_child_weight,
  subsample = xgb_tune3$bestTune$subsample
)

xgb_tune4 <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid4,
  method = "xgbTree",
  verbose = TRUE
)

tuneplot(xgb_tune4)
################################################
tune_grid5 <- expand.grid(
  nrounds = seq(from = 100, to = 10000, by = 100),
  eta = c(0.01, 0.015, 0.025, 0.05, 0.1),
  max_depth = xgb_tune2$bestTune$max_depth,
  gamma = xgb_tune4$bestTune$gamma,
  colsample_bytree = xgb_tune3$bestTune$colsample_bytree,
  min_child_weight = xgb_tune2$bestTune$min_child_weight,
  subsample = xgb_tune3$bestTune$subsample
)

xgb_tune5 <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid5,
  method = "xgbTree",
  verbose = TRUE
)

tuneplot(xgb_tune5)
##################################################
(final_grid <- expand.grid(
  nrounds = xgb_tune5$bestTune$nrounds,
  eta = xgb_tune5$bestTune$eta,
  max_depth = xgb_tune5$bestTune$max_depth,
  gamma = xgb_tune5$bestTune$gamma,
  colsample_bytree = xgb_tune5$bestTune$colsample_bytree,
  min_child_weight = xgb_tune5$bestTune$min_child_weight,
  subsample = xgb_tune5$bestTune$subsample
))

(xgb_model <- caret::train(
  x = input_x,
  y = input_y,
  trControl = train_control,
  tuneGrid = final_grid,
  method = "xgbTree",
  verbose = TRUE
))
############CHECK########################

check=function(l,ans)
{
  score=0
  for(i in 1:length(l))
  {
    if(ans[i]==round(l[i]))
    {
      score=score+1
    }
  }
  print(score/length(l))
}
#1
k=predict(xgb_tune,pred)
write.csv(k,"last.csv")
#2
k2=predict(xgb_tune2,pred)
write.csv(k,"last.csv")

#3
k3=predict(xgb_tune3,pred)
check(k3,ans)

#4
k4=predict(xgb_tune4,pred)
check(k4,ans)

#5
k5=predict(xgb_tune5,pred)
check(k5,ans)

###stacking
m=matrix(c(k,k2,k3,k4,ans),500,5)
train=m[1:400,]
pred=m[401:500,-5]
ans=m[401:500,5]
dat=as.matrix(dat)
train=dat[1:1000,]
pred=dat[1001:1500,-17]
ans=dat[1001:1500,17]
input_x=train[,1:4]
input_y=train[,5]
input_x
xgb_tune_s <- caret::train(
  x = input_x,
  y = input_y,
  tuneGrid = tune_grid,
  method = "xgbTree",
  verbose = TRUE
)
