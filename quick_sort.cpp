#include "quick_sort.h"

vector<int> QuickSort::sort(const vector<int>& array) {
    if (array.size() <= 1) {
        return array;
    }

    vector<int> result = array;

    quick_sort(result, 0, (int)result.size() - 1);
    return result;
}

void QuickSort::quick_sort(vector<int>& array, int left, int right) {
    if (left >= right) { //базовое условие
        return;
    }

    int mid = left + (right - left) / 2;
    int pivot = array[mid]; //выбор опорного элемента - pivot
    int i = left;
    int j = right;

    //разделение
    while (i <= j) {
        while (array[i] < pivot) 
            i++;
        while (array[j] > pivot)
            j--;

        if (i <= j) {
            swap(array[i], array[j]); 
            i++;
            j--;
        }
    }

    //рекурсивно сортируем две части
    quick_sort(array, left, j);
    quick_sort(array, i, right);
}