#include <iostream>
#include <string>
#include <iterator>
#include <algorithm>
#include <list>
#include <vector>
#include <map>
#include <fstream>


void task_1() {
	std::string str_tmplt = "abcdefghijklmnoprstuvwxyz";
	std::string::iterator str_iter;
	std::vector<char> v(str_tmplt.begin(), str_tmplt.end());

	std::cout << "Task #1:" << std::endl;
	std::cout << "Vector in the direct order:  [";
	copy(v.begin(), v.end(), std::ostream_iterator<char>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl;

	std::cout << "Vector in the reverse order: [";
	copy(v.rbegin(), v.rend(), std::ostream_iterator<char>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl << std::endl;

	return;
}


void task_2() {
	std::list<std::string> group1 = {"Jones", "Cormier", "Gustafsson", "Miocic"};
	std::list<std::string> group2 = {"Nurmagomedov", "Ferguson", "McGregor"};
	std::list<std::string> result;

	std::cout << "Task #2:" << std::endl;
	std::cout << "Group 1 list: [";
	copy(group1.begin(), group1.end(), std::ostream_iterator<std::string>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl;

	std::cout << "Group 2 list: [";
	copy(group2.begin(), group2.end(), std::ostream_iterator<std::string>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl;

	std::merge(group1.begin(), group1.end(), group2.begin(), group2.end(), std::back_inserter(result));
	std::cout << "Merged list:  [";
	copy(result.begin(), result.end(), std::ostream_iterator<std::string>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl;

	result.sort();
	std::cout << "Sorted list:  [";
	copy(result.begin(), result.end(), std::ostream_iterator<std::string>(std::cout, ", "));
	std::cout << "\b\b]" << std::endl << std::endl;

	return;
}


class FindWord {
private:
	unsigned int count;
	std::vector<std::string> vector;

public:
	FindWord() {
		this->count = 0;
	}

	void on_find(std::string match_str) {
		this->count++;
		this->vector.push_back(match_str);
	}

	std::vector<std::string> get_vector() {
		return this->vector;
	}

	unsigned int get_count() {
		return this->count;
	}

	std::string on_show() {
		std::string str = this->get_count() ? "Found " + std::to_string(this->get_count()) + " matches" : "Not found";
		return str;
	}
};


std::map<std::string, FindWord> find_in_file(std::istream& input, std::vector<std::string> to_find) {
	std::string line;
	std::vector<std::string> file_lines;
	std::vector<std::string>::iterator iter;
	std::map<std::string, FindWord> matches;
	std::map<std::string, FindWord>::iterator key;

	while(std::getline(input, line)) {
		for(iter=to_find.begin(); iter < to_find.end(); iter++) {
			if(line.find(*iter) != std::string::npos) {
				if(!matches.count(*iter))
					matches.insert(std::pair<std::string, FindWord>(*iter, FindWord()));
				matches.at(*iter).on_find(line);
			}
		}
	}
	
	return matches;
}


void task_3() {
	std::ifstream input("D:\\Univ\\oop\\lab4\\static_demo.cpp");
	std::vector<std::string> vector = {"buff", "return", "class", "locked", "by"};
	std::map<std::string, FindWord> matches;

	std::cout << "Task #3:" << std::endl;
	if(input.is_open()) {
		matches = find_in_file(input, vector);
		input.close();
		for(auto iter=matches.begin(); iter != matches.end(); iter++) {
			std::cout << "Search <" << iter->first << ">: <"  << iter->second.on_show();
			// std::cout << ">, In lines: [";
			// buff = iter->second.get_vector();
			// copy(buff.begin(), buff.end(), std::ostream_iterator<std::string>(std::cout, ", "));
			// std::cout << "\b\b]" << std::endl;
			std::cout << ">" << std::endl;
		}
	}
	else
		std::cout << "No such file or directory!" << std::endl;

	return;
}


int main() {
	task_1();
	task_2();
	task_3();

	return 0;
}