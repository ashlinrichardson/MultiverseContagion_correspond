# essential reading:
#   https://cran.r-project.org/web/packages/V8/vignettes/v8_intro.html

library(Rcpp)
library(V8)

src<-function(x){
  # cat(paste(x, "\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp') ## source c/c++ fxn
}

src("cpp/file_read.cpp") # read file
# file_read("cpp/file_read.cpp") # example use from R
# txt = console.r.call('file_read', xFile) # example call back to R from JS
ctx <- v8()

ctx$assign("use_html", FALSE)
ctx$source("DUALuse.js")




