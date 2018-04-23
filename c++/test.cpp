#include<bits/stdc++.h>
#include "WiSARD.h"
#define n_train 60000
#define n_test 10000
#define tuple_size 28*28
#define path_train_images "../data/mnist/train_images.txt"
#define path_train_labels "../data/mnist/train_labels.txt"
#define path_test_images "../data/mnist/test_images.txt"
#define path_test_labels "../data/mnist/test_labels.txt"
using namespace std;

int main(void){
  FILE *file_images = fopen(path_train_images, "r");
  int **images;
  images = new int*[n_train];
  for(int i=0;i<n_train;i++){
    images[i] = new int[tuple_size];
    for(int j=0;j<tuple_size;j++){
      int x;
      fscanf(file_images, "%d", &x);
      images[i][j] = x;
    }
  }
  fclose(file_images);

  FILE *file_labels = fopen(path_train_labels, "r");
  string *labels;
  labels = new string[n_train];
  for(int i=0;i<n_train;i++){
    int x;
    fscanf(file_labels, "%d", &x);
    labels[i] = to_string(x);
  }
  fclose(file_labels);

  FILE *file_test_images = fopen(path_test_images, "r");
  int **test_images;
  test_images = new int*[n_test];
  for(int i=0;i<n_test;i++){
    test_images[i] = new int[tuple_size];
    for(int j=0;j<tuple_size;j++){
      int x;
      fscanf(file_test_images, "%d", &x);
      test_images[i][j] = x;
    }
  }
  fclose(file_test_images);

  FILE *file_test_labels = fopen(path_test_labels, "r");
  string *test_labels;
  test_labels = new string[n_test];
  for(int i=0;i<n_test;i++){
    int x;
    fscanf(file_test_labels, "%d", &x);
    test_labels[i] = to_string(x);
  }
  fclose(file_test_labels);


  printf("Starting WiSARD...\n");
  WiSARD w(tuple_size, 28);
  w.random_mapping();
  printf("Starting fit...\n" );
  w.fit(n_train, images, labels);
  printf("Fit ended\n");
  //w.print_discriminator();
  printf("Starting classify...\n");
  vector<string> results = w.classify(n_test, test_images);
  printf("Ending classify\n");
  int sum = 0;
  for(int i=0;i<n_test;i++){
    if(results[i]==test_labels[i]){
      sum+=1;
    }
  }
  printf("Precision : %lf\n", double(sum)/double(n_test));
  w.free_space();
  for (int i = 0; i < n_train; i++)
      delete [] images[i];
  delete [] images;
  for (int i = 0; i < n_test; i++)
      delete [] test_images[i];
  delete [] test_images;
  delete [] labels;
  delete [] test_labels;
  return 0;
}
