#include <iostream>
#include <locale>
#include <cstdlib>
#include <ctime>
#include "quick_sort.h"
#include "array.h"
#include "validation.h"
#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>

static void show_menu() {
    cout << "\nБыстрая сортировка\n" << 
        "1. Ввод массива с клавиатуры\n" << 
        "2. Генерация случайного массива\n" << 
        "3. Загрузка массива из файла\n" <<  
        "4. Выход\n" << 
        "Выберите действие: "; 
}

int main() {
    setlocale(LC_ALL, "Russian");
    srand((unsigned)time(0));
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    while (true) {
        show_menu();

        int choice;
        choice = input_check_int();

        if (choice == 4) {
            cout << "Выход из программы\n";
            break;
        }

        vector<int> array;

        switch (choice) {
        case 1:
            array = Array::input_array();
            break;
        case 2:
            array = Array::random_array();
            break;
        case 3: {
            array = Array::load_from_file();
            break;
        }
        default:
            cout << "Неверный выбор! Выберите из предложенных чисел\n";
            continue;
        }

        Array::print_array(array, "Исходный массив: ");

        vector<int> sorted_array = QuickSort::sort(array);

        Array::print_array(sorted_array, "Отсортированный массив: ");

        cout << "Для сохранения данных в файл введите - 1\n" <<
            "Не сохранять - 2\n";
        int save;
        save = input_check_int();

        while (save != 1 && save != 2) {
            cout << "Выберите из предложенных вариантов (Сохранить - 1, Не сохранять - 2)" << endl;
            save = input_check_int();
        }
        if (save == 1) {
            Array::save_to_file(array, sorted_array);
        }
    }

    return 0;
}