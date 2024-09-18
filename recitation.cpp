// Online C++ compiler to run C++ program online
#include <iostream>
using namespace std;

int FiboSum(int num){
    int a = 0, b = 1, sum = 0;
    for(; a < num;){
        if(a%2 == 0){
            sum+=a;
        }
        
        cout<<a<<"\n";
        
        int next = a + b;
        a = b;
        b = next;
    }
    
    return sum;
}

bool isPrime(int n){
    if(n<=1) return false;
    for(int i=2; i*i<=n; i++){
        if(n%2 == 0) return false;
    }
    return true;
}

bool isPrime2(int n){
    for(int temp=n; temp > 0; temp/=10 ){
        cout<<temp<<"\n";
    }
    cout<<"end here\n";
    return true;
}

int sumof(int n, int m){
    int sum = 0;
    for(int i=m; i<n; i+=m){
        sum+=i;
    }
    return sum;
}

int diff(int n){
    int sq_sum = 0, s_square;
    for(int i = 1; i<=n ; i++){
        s_square += i*i;
        sq_sum +=i
    }
    
    sq_sum = sq_sum * sq_sum;
    
    return s_square - sq_sum;
}
int main() {
    // Write C++ code here
    cout << diff(4)<<"\n";
    
    return 0;
}