/*
Name: Zoe Erpelding
Class: CPSC 122, Section 1
Date Submitted: October 9, 2022
Assignment: Project 5
Description: Uses the bubble sort to sort a file
Citation: Uses fileOpen function from B/7-openFileError
*/

#include <iostream>
#include <fstream> 
#include <string>
using namespace std;

void fileOpen (fstream& file, string name, char mode);
void bubbleSort (string array[], int n);
void sink (string array[], int bottom);
void shift (string array[], int current);
void reWrite (string argv, string array[], int length);
int read (string argv1, string array[]);

int main(int argc, char* argv[])
{	
	string array[100];	
	int length = read(argv[1], array);	//read() writes the file into the array and returns the length of numbers
	
	for(int i = 0; i < length; i++)
	//	cout << array[i] << endl;
	
	bubbleSort(array, length);		//sorts the array to be smallest to largest
	reWrite(argv[2], array, length);	//rewrites the sorted array into the input file
	
	for(int j = 0; j < length; j++)
	//	cout << array[j] << endl;
	
	return 0;
}

/*
Description: Reads the numbers from the file titled argv[1] and writes them into an array. Totals up the length of the array while doing it.
Input: the input file name which is argv[1] and an integer array 
Output: alters the empty array and returns the length of numbers in the array
*/
int read (string argv1, string array[])
{
	
	fstream fin;
	fileOpen(fin, argv1, 'r');
	int idx = 0;
	string line;
	while (fin)
	{
		getline(fin, line, '\n');
		array[idx] = line;
		idx++;
	}
	int length = idx - 1;
	fin.close();
	
	return length;
}


/*
Description: rewrites the now sorted numbers of the array into the file titled argv[2]
Input: the output file name argv[2], the now sorted integer array, the integer length of the numbers in the array
Output: writes the array into a file
*/
void reWrite(string argv, string array[], int length)
{
	fstream fout;
	fileOpen(fout, argv, 'w');
	int i = 0;
	while (i < length)
	{
		fout << array[i] << endl;
		i++;	
	}
	fout.close();
}


/*
Description: sorts an array so that it is in order from smallest to largest
Input: the not sorted integer array and the integer length of the array
Output: sorts the array from smallest to largest
*/
void bubbleSort(string array[], int n)
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
void sink (string array[], int bottom)
{
	int current = 0;
	while (current < bottom)
	{
		
		if (array[current].compare(array[current+1]) > 0)
		{	
			//cout << array[current] << " bigger than " << array[current+1] << endl;
			shift(array, current);
		}
		
		current++;
	}
}


/*
Description: Is the simple function of switching the spots of two numbers in an array
Input: the integer array and the index of the current number that you are looking at
Output: switches the number you are looking at with the number following it
*/
void shift (string array[], int current)
{
	string temp = array[current];
	array[current] = array[current + 1];
	array[current + 1] = temp;
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
