/*
Name: Zoe Erpelding
Class: CPSC 122
Date Submitted: September 16, 2022
Assignment: Project 3
Description: Command line will have two digit strings and a name of a file. It will convert the digit strings to integers, multiply them, and place them in the file titled from the command line. 
Citation: Program uses power function from A/ex5.cpp
*/

#include <iostream>
#include <fstream>
using namespace std;


int myAtoi(char str[]);
int myStrnLen(char str[]);
int power(int base, int exp);

int main(int argc, char* argv[])
{
	ofstream fout;
	fout.open(argv[3]);

	int total = myAtoi(argv[1]) * myAtoi(argv[2]);
	fout << total << endl;

 	fout.close(); 
	
 	return 0;
}

/*
Description: Transforms a digit string stored as a c-string to an int.
The function is invoked from main like this:
	int num atoiMy(argv[1]) or int num atoiMY(argv[2])
	argv[1] might look like this: '1' '2' '3' '|0' where each of the four characters are stored in a character array
Input: c-string containing digits
Returns: integer value of the c-string
*/
int myAtoi(char str[])
{
	int length = myStrnLen(str);
	int i = 0;
	int num = 0; 
	int place = 1;
	
	while(str[i] != '\0')
	{		
		int exp = power(10, length - place);
		int value = str[i] - 48; 
		num = num + value*exp;
		i++;
		place++;
	}
	
	return num;
}


/*
Description: Computes the number of characters in a c-string excluding the null terminator ('\0') 
Input: c-string
Returns: number of characters in the c-string excluding the null terminator ('\0')
*/
int myStrnLen(char str[])
{
	int i=0;
	while(str[i] != '\0')
		i++;	
	
	return i;
}


/*
Description: Raises a number to an exponent
Input: base integer and exponent integer
Returns: the value of this computation
*/
int power(int base, int exp)
{
 	int value = 1;
	for (int i = 0; i < exp; i++)
		value = value * base;
	
	return value;
}





