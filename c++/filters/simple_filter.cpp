#include<bits/stdc++.h>
#define tuple_size (256*256)
#define n_images 213
int x;
int main(){
  for(int i=0;i<n_images;i++){
    for(int j=0;j<tuple_size;j++){
      scanf("%d", &x);
      if(x>75){printf("1 ");}
      else{printf("0 ");}
    }
    printf("\n");
  }

  return 0;
}
