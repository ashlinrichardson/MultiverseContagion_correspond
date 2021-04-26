#include<Rcpp.h>
#include<stdio.h>
#include<stdlib.h>

using namespace std;
using namespace Rcpp;

size_t file_size(const char * fn){
  FILE * f = fopen(fn, "rb");
  if(!f){
    printf("Error: failed to open file: %s\n", fn);
    exit(1);
  }
  fseek(f, 0L, SEEK_END);
  size_t s = ftell(f);
  fclose(f);
  return s;
}

//[[Rcpp::export]]
String file_read(String args){
  std::string fn = args;
  size_t fs = file_size(fn.c_str()); // get file size
  size_t bs = fs * sizeof(char); // buffer size to allocate
  char * s = (char *) (void *) malloc(bs); // allocate buffer
  memset(s, '\0', bs); // touch buffer area with null, auto null-terminated

  FILE * f = fopen(fn.c_str(), "rb"); // read file
  size_t n_r = fread(s, fs, sizeof(char), f);
  fclose(f);

  string ret(s);
  free(s);

  return String(ret); // convert c string to r-native object
}
