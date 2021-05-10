#ifndef __mapreduce_h__
#define __mapreduce_h__

#include <stdio.h>

// MR needs to access the pagerank vector, which is in 03_pagerank.cpp
extern double* pagerank_vector[2];
extern unsigned int newArrayNum;
extern const double b;
extern const double e;

// Different function pointer types used by MR
typedef double (*Getter)(char *key, int partition_number);
typedef void (*Mapper)(char *file_name);
typedef void (*Reducer)(char *key, Getter get_func, int partition_number);
typedef unsigned long (*Partitioner)(char *key, int num_partitions);

// External functions: these are what you must define
void MR_Emit(char *key, double value);

unsigned long MR_DefaultHashPartition(char *key, int num_partitions);

void MR_Run(FILE* input, 
	    Mapper map, int num_mappers, 
	    Reducer reduce, int num_reducers, 
	    Partitioner partition);

#endif // __mapreduce_h__
