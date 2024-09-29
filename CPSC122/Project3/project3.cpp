/*
Name: Zoe Erpelding
Class: CPSC 122, Section 1
Date Submitted: September 23, 2022
Assignment: Project 3
Description: Uses the substitution cipher to encrypt/decrypt a file
Citation: Uses fileOpen function from B/7-openFileError and code from B/5-ioChar
*/



#include <iostream>
#include <fstream> 
#include <cstdlib>  //necessary for the constant EXIT_FAILURE and rand()
#include <ctime>  // for time
#include <string>
using namespace std;

char decrypt(char, int);
void decryptCipherText(string, string, string);
char encrypt(char, int);
void encryptPlainText(string, string, string);
void fileOpen(fstream&, string, char);
int keyGen(string);
bool passOver(char);
int readKey(string);
void toBlock(string);

int main(int argc, char* argv[])
{
	
	int command = atoi(argv[1]);
	
	if (command == 0)
	{
		keyGen(argv[2]);  // keyFile
	}
	
	
	else if (command == 1)
	{
		encryptPlainText(argv[2], argv[3], argv[4]);  // keyFile, plain text file, encrypted text file
	}
	
	else if (command == 2)
	{
		decryptCipherText(argv[2], argv[3], argv[4]);  // keyFile, encryped text file, decrypted text file
	}
	
	else 
	{
		cout << "Must specify requested action by typing 0, 1, or 2" << endl;
	}
		
	return 0;
}

/*
Description: Decrypts an upper case alphabetic character using the Caesar cipher
Input: upper case alphabetic character, valid key
Returns: decrypted version of input 
*/
char decrypt(char ch, int key)
{
	int pos = ch - 'A';
	pos = (pos - key + 26) % 26;
	ch = pos + 'A';
	return ch;
}


/*
Description: Is called when command is (2) and decrypts the full text
Input: 3 strings: argv[2], argv[3], argv[4]
Returns: none
*/
void decryptCipherText(string argv2, string argv3, string argv4)
{
	fstream fin;
	fstream fout;	
		
	fileOpen(fin, argv3, 'r');
	fileOpen(fout, argv4, 'w');
	
	int key = readKey(argv2);
	
	while(fin.peek() != EOF)
 	{
 		char ch = fin.get();
 		if(isalpha(ch))
 			fout.put(decrypt(ch, key));
   		else
  			fout.put(ch);
 	}
		
	fin.close();
	fout.close();
}

/*
Description: Encrypts an upper case alphabetic character using the Caesar cipher
Input: upper case alphabetic character, valid key
Returns: encrypted version of ch
*/
char encrypt(char ch, int key)
{
	int pos = ch - 'A';
	pos = (pos + key) % 26;
	ch = pos + 'A';
	return ch;
}

/*
Description: Is called when the command is (1) and encrypts the plaintext
Input: Three strings: should be argv[2], argv[3], argv[4]
Output: none
*/
void encryptPlainText(string argv2, string argv3, string argv4)
{
	fstream fin;
	fstream fout;
	
	fileOpen(fin, argv3, 'r');
	toBlock(argv3);
	fin.close();
		
	fileOpen(fout, argv4, 'w');		
	fileOpen(fin, "BTFile.out", 'r');
		
	int key = readKey(argv2);
		
	while(fin.peek() != EOF)
 	{
 		char ch = fin.get();
 		if(isalpha(ch))
 			fout.put(encrypt(ch, key));
   		else 
  			fout.put(ch);
 	}
		
	fin.close();
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


/*
Description: Randomly generates an integer in the range: [1..25]
Input: name of keyFile
Output: Stores randomly generated integer in keyFile
*/
int keyGen(string keyFile)
{
	//seed the pseudo random number generation so that subsequent runs will generate a different sequence
 	unsigned seed = time(NULL);
 	srand(seed); 
 	
	int key = rand() % 26;
	
	ofstream fout;
	fout.open(keyFile);
	fout << key << endl;
	fout.close();
	
	return 0;
}

/*
Description: Returns a bool of whether the character should be passed over or not
Input: character from file
Output: a true or false value
*/
bool passOver(char ch)
{
	bool pass = false;
	if (ch == '.' or ch == ',' or ch == ' ' or ch == '\n')
		pass = true;
	
	return pass;
}

/*
Description: Reads the number located in the keyFile
Input: string name of keyFile
Output: the integer number located in keyFile
*/
int readKey(string keyFile)
{
	fstream fin;
	fileOpen(fin, keyFile, 'r');
	int key;
	fin >> key;	
	fin.close();
	return key;	
}


/*
Description: Transforms PTFile into block text
Input: name of PTfile, BKfile
Output: BKfile contains block text version of PTFile
BKfile is a hard-coded constant file name
Block text has:
1. periods, commas, spaces removed
2. all alphabetic characters are upper case
3. no more than 50 characters per line
*/
void toBlock(string PTFile)
{
	fstream fin;
	fstream fout;
	
	fileOpen(fin, PTFile, 'r');
	fileOpen(fout, "BTFile.out", 'w');	

	int ct = 0;
	
	while(fin.peek() != EOF)
 	{
  		char ch = fin.get();
  		if (passOver(ch) == false)
  		{
  			if (isalpha(ch))
  			{
   				ch = toupper(ch);
   				fout.put(ch);   
   				ct ++;
   			}
   			else
   			{
   				fout.put(ch);
  				ct++;
  			}
  			if (ct % 50 == 0)
   				fout.put('\n');	
  		}		
  	}
  		
 	fout.put('\n'); 
	
	fin.close();
	fout.close();
}



