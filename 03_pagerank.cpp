#include <iostream>
#include <fstream>
#include <sstream>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstring>
#include <math.h>
#include "mapreduce.h"
using namespace std;

// constants
const double b = 0.85; // beta
const double e = 0.01;  // epsilon

// pagerank vector
double* pagerank_vector[2];
uint newArrayNum = 1;
    
void Map(char *line) {
    {
        char *c = line;
        while (*c != '\0') {
            if (*c == '\n'){
                *c = '\0';
                break;
            }
            ++c;
        }
    }

    uint arrayNum = (newArrayNum == 1) ? 0 : 1;
    int src, deg;
    char* dst;
    double val;
    char* num = strtok(line, " ");
    assert(num != NULL);
    src = atoi(num);
    
    num = strtok(NULL, " ");
    assert(num != NULL);
    deg = atoi(num);

    val = b * pagerank_vector[arrayNum][src] / deg;
    for (int i = 0; i < deg; ++i) {
        dst = strtok(NULL, " ");
        MR_Emit(dst, val);
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

int main(int argc, char* argv[]) {
    FILE* edges = fopen("./edges", "r");
    if (!edges) {
        cout << "Error: cannot open file \"edges\"";
        return 0;
    }

    size_t line_buf_sz = 768;
    char* line = (char*)malloc(sizeof(char) * line_buf_sz);
    uint num_nodes = -1;
    getline(&line, &line_buf_sz, edges);
    getline(&line, &line_buf_sz, edges);
    num_nodes = stoi(string(line));
    assert(num_nodes > 0);
    getline(&line, &line_buf_sz, edges);
    free(line);

    // remember the current "edges" position for multiple MR passes
    long startingPoint = ftell(edges);
    
    double num_nodes_reci = 1/(double)num_nodes;
    for (int i = 0; i < 2; ++i) {
        pagerank_vector[i] = new double[num_nodes];
    }

    // init value
    for (uint i = 0; i < num_nodes; ++i) 
        pagerank_vector[0][i] = num_nodes_reci;
    memset(&pagerank_vector[1][0], 0, sizeof(double) * num_nodes);

    // do pagerank calculation recursively until diff is less than e.
    double diff = e + 1;
    do {
        MR_Run(edges, Map, 1, Reduce, 1, MR_DefaultHashPartition);
        double newSum = 0;
        for(uint i = 0; i < num_nodes; ++i) {
            newSum += pagerank_vector[newArrayNum][i];
        }
        assert(newSum <= 1.01);
        newSum = (1 - newSum) / num_nodes;
        for(uint i = 0; i < num_nodes; ++i) {
            pagerank_vector[newArrayNum][i] += newSum;
        }

        // calc diff
        double newDiff = 0;
        for(uint i = 0; i < num_nodes; ++i) {
            newDiff += fabs(pagerank_vector[0][i] - pagerank_vector[1][i]);
        }
        diff = newDiff;

        // lastly: change the next input array; fseek "edges" to the correct position
        newArrayNum = (newArrayNum == 1) ? 0 : 1;
        fseek(edges, startingPoint, SEEK_SET);
    }
    while(diff >= e);

    // save the result
    fstream pagerank("./pagerank", ios_base::out);
    int arrayNum = (newArrayNum == 1) ? 0 : 1;
    for(uint i = 0; i < num_nodes; ++i) {
        pagerank << i << " " << pagerank_vector[arrayNum][i] << endl;
    }
    pagerank.close();

    // pagerank.open()

    // free memory
    for (int i = 0; i < 2; ++i) {
        delete pagerank_vector[i];
    }

    return 0;
}