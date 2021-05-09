#include <iostream>
#include <fstream>
#include <sstream>
#include <assert.h>
#include <cstring>
using namespace std;

// constants
const double b = 0.85; // beta
const double e = 0.1;  // epsilon

int main(int argc, char* argv[]) {
    fstream edges("./edges");
    if (!edges.is_open()) {
        cout << "Error: cannot open file \"edges\"";
        return 0;
    }

    string s;
    stringstream ss(s);
    uint num_nodes = -1;
    getline(edges, s);
    getline(edges, s);
    ss >> num_nodes;
    assert(num_nodes > 0);
    getline(edges, s);
    
    double num_nodes_reci = 1/(double)num_nodes;
    bool newArray = 1;
    double** pagerank_vector = new double*[2];
    for (int i = 0; i < 2; ++i) {
        pagerank_vector[i] = new double[num_nodes];
    }
    // init value
    for (int i = 0; i < num_nodes; ++i) 
        pagerank_vector[0][i] = num_nodes_reci;
    memset(&pagerank_vector[1], 0, sizeof(double) * num_nodes);

    // 

    // free memory
    for (int i = 0; i < 2; ++i) {
        delete pagerank_vector[i];
    }
    delete pagerank_vector;

    return 0;
}