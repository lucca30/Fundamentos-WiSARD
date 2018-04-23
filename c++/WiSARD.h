#include<bits/stdc++.h>
#include <random>       // std::default_random_engine
#include <chrono>       // std::chrono::system_clock
using namespace std;
typedef unsigned long long int ull;
class WiSARD{
  public:
    int input_size;
    int ram_size;
    int n_rams; //number of rams
    int mask_size;
    int** mapa; //mapa[i][j]=k indicate that the k-th pixel of input will be used in the i-th RAM, in the j-th position
    map<string, vector<map<vector<ull>, int > > > discriminators; // first key is the class, second key is the bitmask (represented by a vector of 64 bits integers)
    WiSARD(int input_size,int ram_size);
    void random_mapping(void);
    void simple_mapping(void);
    void free_space(void);
    void print_discriminator(void);
    void fit(int train_size, int** input_tuple, string* input_label);
    vector<string> classify(int test_size, int** input_tuple);
};
