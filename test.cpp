#include "gtest/gtest.h"
#include "quick_sort.h"

using namespace std;

TEST(QuickSort_test, positive_num) {
    vector<int> arr = { 1, 5, 3, 9, 6, 33 };
    vector<int> expected = { 1, 3, 5, 6, 9, 33 };
    vector<int> result = QuickSort::sort(arr);
    EXPECT_EQ(arr, arr);
}
TEST(QuickSort_test, negative_num) {
    vector<int> arr = { -1, -5, -3, -9, -6, -33 };
    vector<int> expected = { -33, -9, -6, -5, -3, -1 };
    vector<int> result = QuickSort::sort(arr);
    EXPECT_EQ(result, expected);
}
TEST(QuickSort_test, identical_num) {
    vector<int> arr = { 5, 5, 5, 5 };
    vector<int> expected = { 5, 5, 5, 5 };
    vector<int> result = QuickSort::sort(arr);
    EXPECT_EQ(arr, expected);
}

TEST(QuickSort_test, single_element) {
    vector<int> arr = { 42 };
    vector<int> expected = { 42 };
    vector<int> result = QuickSort::sort(arr);
    EXPECT_EQ(result, expected);
}

TEST(QuickSort_test, empty_array) {
    vector<int> arr = {};
    vector<int> expected = {};
    vector<int> result = QuickSort::sort(arr);
    EXPECT_EQ(result, expected);
}