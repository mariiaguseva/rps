#pragma once
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <ctime>
using namespace std;

class Array {
public:
    static vector<int> input_array();
    static vector<int> random_array();
    static vector<int> load_from_file(); 
    static void save_to_file(const vector<int>& original, const vector<int>& sorted);
    static void print_array(const vector<int>& arr, const string& name);
};
