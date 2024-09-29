/*
Name: Zoe Erpelding
Class: CPSC 122, Section 1
Date: September 9, 2022
Assignment: Project 1
Description:  Program prints n prime numbers in columns of c. n and c are the second and third command line arguments respectively.
Citation: Uses code from ex4.cpp and ex6.cpp
*/


#include <iostream>
using namespace std;

bool isPrime(int num);
void display(int totalPrimes, int cols);
void error(int code);

int main(int argc, char* argv[]){
 
 	// Amount of prime numbers and number of columns are taken from the command line
	int totalPrimes = atoi(argv[1]);		
	int columns = atoi(argv[2]);	
	
	// Error checking
	if (totalPrimes < 1){
		error(1);
	}
	if (columns < 1){
		error(2);
	}
	
	// Create prime table
	display(totalPrimes,columns);
	cout << endl;

	return 0;
} 


/*
Description: Determines whether input integer is prime
Input: integer whose primality is to be judged
Returns: true if num is prime, false otherwise
*/
bool isPrime(int num){
	bool prime = false;
	int remainder = 1;
	
	// This for loop will divide a number to find it's remainder until it finds that the number can be evenly divisible by something, or until it runs out of numbers to divide it by			
	for (int j = 2; j < num; j++){		
		remainder = num % j;		
		if (remainder == 0){
			break;						
		}
	}

	// It will only change the value of prime to true if it is a prime number since numbers that can be evenly divided will have a remainder of 0 after they break from the for loop above.			
	if (remainder != 0){			
		prime = true;
	}
	
	return prime;
}

/*
Description: Loops over all necessary candidate primes, invoking isPrime on each, displaying in column fashion those that are prime
Input: integer totalPrimes, indicating the number of primes to display; integer cols, indicating over how many columns the primes are to be displayed 
*/
void display(int totalPrimes, int cols){

	int num = 2;
	int count = 0;
 
	while (count < totalPrimes){
		if(isPrime(num)){
			cout << num << '\t';  
			count++;
			if (count % cols == 0){  
				cout << endl;
			}
		}
		num++;
	}  

}

/*
Description: Writes the appropriate error into the terminal
Input: the integer that represents which number has been incorrectly typed into the command line (either numbers displayed or columns)
*/
void error(int code){
	if (code == 1){
   		cout <<  "Numbers displayed must be greater than or equal to 1" << endl;
   		exit(EXIT_FAILURE);
  	}
 	
 	if (code == 2){
   		cout <<  "Columns must be greater than or equal to 1" << endl;
   		exit(EXIT_FAILURE);
  	}

}


