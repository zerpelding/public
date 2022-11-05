/*
Name: Zoe Erpelding
Class: CPSC 122, Section 1
Date Submitted: October 22, 2022
Assignment: Project 7
Description: Uses the bubble sort to sort numbers in an array and then search for a target using binary search
Citation: Uses binS found in 2-BinarySrch
*/

#include <iostream>
#include <string>
#include <fstream>
using namespace std;

void bubbleSort (int* array, int n);
void sink (int* array, int bottom);
void shift (int* array, int current);
void loadArray(int* array, int size, int limit);
bool binarySearch(int* array, int size, int target);
void out(int* array, int size, string argv4);
void fileOpen(fstream& file, string name, char mode);

int main(int argc, char* argv[])
{
	int size = atoi(argv[1]);
	int limit = atoi(argv[2]);
	int target = atoi(argv[3]);
	int* array = new int[size];	//dynamically declares array
	
	loadArray(array, size, limit);	//loads the array with numbers
	bubbleSort(array, size);		//sorts the array to be smallest to larges
	out(array, size, argv[4]);		//writes sorted array into file
		
	if(binarySearch(array, size, target))	//look for target with binary search function
		cout << target << " found" << endl;
	else
		cout << target << " not found" << endl;
	
	
	return 0;
}

/*
Description: searches for a target inside of a sorted array using binary search
Input: the array, the size of the array, the number you are looking for in the array
Ouput: returns true if the number is found and false if it is not found in the array
*/
bool binarySearch(int* array, int size, int target)
{
	bool found = false;
	
	int bottom = size - 1;
	int top = 0;
	int middle;
	
	while (top <= bottom)
	{
		middle = (top + bottom)/2;
		
		if (array[middle] == target)
		{
			found = true;
			break;
		}
		if (target < array[middle])
			bottom = middle - 1;
		else
			top = middle + 1;
	}
	
	return found;
}


/*
Description: adds "size" random numbers to the array (less than or equal to the limit number)
Input: the array, how many numbers should be in the array, the largest number allowed in the array
Output: fills the array with numbers
*/
void loadArray(int* array, int size, int limit)
{
	unsigned seed = time(NULL);
 	srand(seed); 
 	
	for (int i = 0; i < size; i++)
		array[i] = rand() % (limit + 1);
	
}


/*
Description: sorts an array so that it is in order from smallest to largest
Input: the not sorted integer array and the integer length of the array
Output: sorts the array from smallest to largest
*/
void bubbleSort(int* array, int n)
{
	int pass = 0;
	int bottom = n - 1;
	while (pass < n-1)
	{
		sink(array, bottom);
		bottom--;
		pass++;
	}	
}

/*
Description: switched two numbers in the array if the first number is bigger than the second number (sinks the bigger number down by one spot)
Input: the integer array and the index of the bottom integer (initialized in bubbleSort)
Output: switches two numbers in the array if appropriate
*/
void sink (int* array, int bottom)
{
	int current = 0;
	while (current < bottom)
	{
		if (array[current] > array[current + 1])
			shift(array, current);
		current++;
	}
}

/*
Description: Is the simple function of switching the spots of two numbers in an array
Input: the integer array and the index of the current number that you are looking at
Output: switches the number you are looking at with the number following it
*/
void shift (int* array, int current)
{
	int temp = array[current];
	array[current] = array[current + 1];
	array[current + 1] = temp;
}

/*
Description: writes the array into a file
Input: the name of the array, the size of te array, the name of the file to print to
Output: writes array into file
*/
void out(int* array, int size, string argv4)
{
	fstream fout;
	fileOpen(fout, argv4, 'w');
	int i = 0;
	while (i < size)
	{
		fout << array[i] << endl;
		i++;	
	}
	fout.close();
}

/*
Description: function opens a file 
Input: file stream object reference, name of the file, mode of open
Output: input file name is opened
*/ 
void fileOpen(fstream& file, string name, char mode)
{
 	string fileType;
 	if (mode == 'r')
  		fileType = "input";
 	if (mode == 'w')
  		fileType = "output";
 	if (mode == 'r')
  		file.open(name, ios::in);
 	else
  		if (mode == 'w')
   			file.open(name, ios::out);  
 	if (file.fail()) //error condition 
 	{
  		cout << "Error opening " << fileType << " file" << endl; 
  		exit(EXIT_FAILURE);
 	}
}


