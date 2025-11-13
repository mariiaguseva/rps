#include "array.h"
#include "validation.h"

vector<int> Array::input_array() {
    vector<int> numbers;
    string input;

    while (true) {
        cout << "Введите целые числа через пробел: ";
        getline(cin, input);

        stringstream ss(input);
        int num;

        numbers.clear();

        while (ss >> num) {
            numbers.push_back(num);
        }

        if (!ss.eof()) {
            cout << "Ошибка! Обнаружены недопустимые символы.\n";
        }
        else {
            break;
        }
    }

    return numbers;
}

vector<int> Array::random_array() {
    int count;
    cout << "Сколько чисел сгенерировать? ";
    count = input_check_int();
  
    vector<int> numbers;
    for (int i = 0; i < count; i++) {
        numbers.push_back(rand() % 100 + 1);
    }

    return numbers;
}

vector<int> Array::load_from_file() {
    string filename;

    cout << "Введите путь к файлу: ";
    getline(cin, filename);

    //убираем кавычки если есть
    string cleaned_filename;
    for (char c : filename) {
        if (c != '"') {
            cleaned_filename += c;
        }
    }
    cleaned_filename = name_validity(cleaned_filename); 

    ifstream file;
    file.open(cleaned_filename);

    while (!file.is_open()) {
        cout << "Ошибка открытия файла" << endl;
        cout << "Введите корректный путь к файлу: ";
        getline(cin, filename);

        cleaned_filename.clear();
        for (char c : filename) {
            if (c != '"') {
                cleaned_filename += c;
            }
        }
        file.open(cleaned_filename);
    }

    if (file.eof()) {
        cout << "\nФайл пустой.\n" << endl;
        file.close();
        return vector<int>();
    }

    vector<int> numbers;
    int num;

    while (file >> num) {
        numbers.push_back(num);
    }

    if (file.fail() && !file.eof()) {
        cout << "Ошибка. В файле содержатся недопустимые данные.\n";
        numbers.clear();
    }

    file.close();
    return numbers;
}

void Array::save_to_file(const vector<int>& original, const vector<int>& sorted) {
    string filename;

    cout << "Введите путь к файлу: ";
    getline(cin, filename);


    string cleaned_filename;
    for (char c : filename) {
        if (c != '"') {
            cleaned_filename += c;
        }
    }
    cleaned_filename = name_validity(cleaned_filename); 

    //добавляем расширение 
    string final_filename = cleaned_filename;
    if (final_filename.find('.') == string::npos) {
        final_filename += ".txt";
    }

    ofstream file(final_filename);

    if (!file.is_open()) {
        cout << "Ошибка создания файла!" << endl;
        return;
    }

    for (int num : original) {
        file << num << " ";
    }
    file << "\n";

    for (int num : sorted) {
        file << num << " ";
    }
    file << "\n";

    file.close();
    cout << "Результаты сохранены в файл: " << final_filename << "\n";
}

void Array::print_array(const vector<int>& arr, const string& name) {
    cout << name;
    for (int num : arr) {
        cout << num << " ";
    }
    cout << "\n";
}