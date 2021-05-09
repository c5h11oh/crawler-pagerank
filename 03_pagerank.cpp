#include <iostream>
#include <fstream>
#include <sstream>
#include <assert.h>
#include <stdio.h>
#include <cstring>
#include "mr/mapreduce.h"
using namespace std;

// constants
const double b = 0.85; // beta
const double e = 0.1;  // epsilon

// pagerank vector
double* pagerank_vector[2];

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
    
    double num_nodes_reci = 1/(double)num_nodes;
    bool newArray = 1;
    for (int i = 0; i < 2; ++i) {
        pagerank_vector[i] = new double[num_nodes];
    }
    // init value
    for (int i = 0; i < num_nodes; ++i) 
        pagerank_vector[0][i] = num_nodes_reci;
    memset(&pagerank_vector[1], 0, sizeof(double) * num_nodes);

    // call map reduce recursively

    // free memory
    for (int i = 0; i < 2; ++i) {
        delete pagerank_vector[i];
    }

    return 0;
}