#include "validation.h"

int input_check_int() {
    int input;
    while (!(cin >> input) || cin.get() != '\n') {
        cin.clear(); // сбрасываем флаги ошибок
        while (cin.get() != '\n'); // очищаем буфер
        cout << "Ошибка ввода! Введите допустимое значение:" << endl;
    }
    return input;
}

string name_validity(string file_name) {
    vector<string> ban_name = {
       "con", "prn", "aux", "nul", "com1", "com2", "com3", "com4",
       "com5", "com6", "com7", "com8", "com9", "lpt1", "lpt2",
       "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"
    };

    bool check;

    do {
        check = true;

        //извлекаем имя файла из пути
        string name = file_name;
        size_t found_check = file_name.find_last_of("\\/");
        if (found_check != string::npos) {
            name = file_name.substr(found_check + 1);
        }

        //убираем расширение
        string only_name = name;
        size_t found_check_1 = name.find_last_of('.');
        if (found_check_1 != string::npos) {
            only_name = name.substr(0, found_check_1);
        }

        //приводим к нижнему регистру
        string lower_name = only_name;
        for (char& c : lower_name) {
            c = tolower(c);
        }

        for (const auto& banned : ban_name) {
            if (lower_name == banned) {
                cout << "Имя файла зарезервировано системой!" << endl;
                cout << "Введите допустимое имя файла: ";
                getline(cin, file_name);
                check = false;
                break;
            }
        }

    } while (!check);

    return file_name;
}