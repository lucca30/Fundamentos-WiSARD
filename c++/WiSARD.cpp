#include<bits/stdc++.h>
#include <random>       // std::default_random_engine
#include <chrono>       // std::chrono::system_clock
#define pb push_back
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

//ok
WiSARD::WiSARD (int input_size,int ram_size){
  this->input_size = input_size;
  this->ram_size   = ram_size;
  if(input_size%ram_size != 0 ){
    puts("-----ERROR in the RAM size-----");
  }
  else{
    this->n_rams  = input_size/ram_size;
    this->mask_size = ram_size/64 + (ram_size%64?1:0);
  }
  this->mapa = new int*[this->n_rams];
  for(int i=0;i<this->n_rams;i++){
    this->mapa[i] = new int[this->ram_size];
  }
}

//ok
void WiSARD::free_space(void){
  for (int i = 0; i < this->n_rams; i++)
      delete [] this->mapa[i];
  delete [] this->mapa;
}

//ok
void WiSARD::random_mapping(void){
  int *temp_pixels = new int[this->input_size];
  for(int i=0;i<this->input_size;i++){
    temp_pixels[i] = i;
  }

  unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
  shuffle (temp_pixels, temp_pixels+this->input_size, default_random_engine(seed));

  for(int i=0;i<this->n_rams;i++){
    for(int j=0;j<this->ram_size;j++){
      this->mapa[i][j] = temp_pixels[i*this->ram_size+j];
    }
  }

  //DEBUG ------START-------------------
/*
  for(int i=0;i<this->n_rams;i++){
    for(int j=0;j<this->ram_size;j++){
      //printf("%d ", this->mapa[i][j]);
    }
    //printf("\n");
  }
*/
  //DEBUG -----END---------------------
  delete [] temp_pixels;
}

void WiSARD::simple_mapping(void){

  for(int i=0;i<this->n_rams;i++){
    for(int j=0;j<this->ram_size;j++){
      this->mapa[i][j] = i*this->ram_size + j;
    }
  }
  //DEBUG -------START-------------
/*
  for(int i=0;i<this->n_rams;i++){
    for(int j=0;j<this->ram_size;j++){
      //printf("%d ", this->mapa[i][j]);
    }
    //printf("\n");
  }
*/
  //DEBUG -------END---------------
}

void WiSARD::fit(int train_size, int** input_tuple, string* input_label){
  for(int i=0;i<train_size;i++){
    //printf("Treino : %d\n", i);
    //printf("Tupla: ");
    //for(int m=0;m<this->input_size;m++){//printf("%d ", input_tuple[i][m]);}
    //printf("\n");
    if(this->discriminators.find(input_label[i])==this->discriminators.end() ){
      this->discriminators[input_label[i]] = vector<map<vector<ull>, int > >(this->n_rams);
    }
    for(int j=0;j<this->n_rams;j++){
      //printf("  RAM:%d\n", j);
      //defining the mask
      vector<ull> mask(this->mask_size);
      fill(mask.begin(),mask.end(), 0);
      //printf("   Len mask: %d\n", mask.size());

      for(int k=0;k<this->ram_size;k++){
        int mask_pos1  = k/64;
        int mask_pos2  = k%64;
        if(input_tuple[i][ this->mapa[j][k] ]){
          //printf("Escrevendo pixel na mascara\n");
          //printf("mask_pos1: %d\n", mask_pos1);
          //printf("mask_pos2: %d\n", mask_pos2);
          //printf("Máscara antes: %llu\n", mask[0]);
          //printf("Pixel usado no or: %d\n", (1 << mask_pos2));
          mask[mask_pos1] = mask[mask_pos1] | (1 << mask_pos2);
          //printf("Máscara depois: %llu\n", mask[0]);
        }
      }
      //printf("   Mask: %llu\n", mask[0]);

      //writing in the j-th RAM of the discriminator
      if(this->discriminators[input_label[i]][j].find(mask) == this->discriminators[input_label[i]][j].end() ){
        this->discriminators[input_label[i]][j][mask] =  1;
      }
      else{
        this->discriminators[input_label[i]][j][mask] += 1;
      }

    }

  }

}

void WiSARD::print_discriminator(void){
  map<string, vector<map<vector<ull>, int > > >::iterator it;
  for(it = this->discriminators.begin();it!=this->discriminators.end();++it){
    printf("Discriminator :");
    cout << it->first << endl;

    for(int i=0;i<this->ram_size;i++){
      printf("  RAM:%d\n", i);
      map<vector<ull> ,int >::iterator it_;
      for(it_ = (it->second)[i].begin();it_!=(it->second)[i].end();++it_){
        printf("%llu(%d) ", (it_->first)[0], it_->second);
      }
      printf("\n");
    }

  }
}

vector<string> WiSARD::classify(int test_size, int** input_tuple){
  vector<string> ans;
  int max_bleaching = 0;
  for(int i=0;i<test_size;i++){
    map<string, vector<map<vector<ull>, int > > >::iterator it;
    map<string ,vector<int> > occurrences;

    //obtaining the value of each ram of each discriminator
    for(it = this->discriminators.begin();it!=this->discriminators.end();++it){
      occurrences[it->first] = vector<int>(this->n_rams);
      for(int j=0;j<this->n_rams;j++){
        //obtaining the mask
        vector<ull> mask(this->mask_size);
        fill(mask.begin(),mask.end(), 0);

        for(int k=0;k<this->ram_size;k++){
          int mask_pos1  = k/64;
          int mask_pos2  = k%64;
          if(input_tuple[i][ this->mapa[j][k] ]){
            mask[mask_pos1] = mask[mask_pos1] | (1 << mask_pos2);
          }
        }

        if( (it->second)[j].find(mask) == (it->second)[j].end() ){
          occurrences[it->first].pb(0);
        }
        else{
          occurrences[it->first].pb((it->second)[j][mask]);
          max_bleaching = max(max_bleaching, (it->second)[j][mask]);
        }

      }
      sort(occurrences[it->first].begin(), occurrences[it->first].end());

      }

      //choosing the best class iterating by the bleaching number
      for(int j=1;j<=max_bleaching;j++){
        vector<pair<int, string> > results;
        map<string ,vector<int> >::iterator it_;
        for(it_ = occurrences.begin();it_!=occurrences.end();++it_){
          int score = (it_->second).size() - (lower_bound((it_->second).begin(), (it_->second).end(), j) - (it_->second).begin());
          results.pb(make_pair(score, it_->first));
        }
        sort(results.begin(), results.end());
        if( (results[results.size()-1].first != results[results.size()-2].first) || j==max_bleaching ){
          ans.pb(results[results.size()-1].second);
          break;
        }

      }


  }
  return ans;
}
