#include "mapreduce.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void Map(char *line) {
    int src, deg;
    char* dst;
    double val;
    char* num = strtok(line, " ");
    assert(num != NULL);
    src = atoi(num);

    num = strtok(NULL, " ");
    assert(num != NULL);
    deg = atoi(num);

    val = b * pagerank_vector[newArrayNum ? 0 : 1][src] / deg;
    for (int i = 0; i < deg; ++i) {
        dst = strtok(NULL, " ");
        MR_Emit(strdup(dst), val);
    }
}

void Reduce(char *key, Getter get_next, int partition_number) {
    int keyInt = atoi(key);
    double newSum = 0;
    double value;
    while ((value = get_next(key, partition_number)) >= 0)
        newSum += value;
    pagerank_vector[newArrayNum][keyInt] = newSum;
}
