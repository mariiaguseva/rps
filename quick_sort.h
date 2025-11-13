#pragma once
#include <vector>
#include <algorithm>
using namespace std;

class QuickSort {
public:
    static vector<int> sort(const vector<int>& arr); 
  
private:
    static void quick_sort(vector<int>& vec, int low, int high);
};