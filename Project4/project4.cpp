/*
Name: Zoe Erpelding
Class: CPSC 122, Section 1
Date Submitted: October 2, 2022
Assignment: Project 4
Description: Uses the affine cipher to encrypt/decrypt a file
Citation: Uses fileOpen function from B/7-openFileError and code from B/5-ioChar
*/

#include <iostream>
#include <fstream> 
#include <cstdlib>  // necessary for the constant EXIT_FAILURE and rand()
#include <ctime>  // for time
#include <string>
using namespace std;

void keyGen (string keyFile);
char encrypt (char ch, int alpha, int beta);
char decrypt (char ch, int alpha, int beta);
void fileControl (string keyFile, string fileIn, string fileOut, int mode);
void fileOpen(fstream&, string name, char mode);
void encryptPlainText(string, string, string);
void decryptCipherText(string, string, string);

// Global constants of the MyInverseAlpha and the p that is called in the decrypt function
const int MI[] = {0,1,0,9,0,21,0,15,0,3,0,19,0,0,0,7,0,23,0,11,0,5,0,17,0,25};
const int p = 25;

int main(int argc, char* argv[])
{
	int command = atoi(argv[1]);	//0 creates key, 1 encrypts, 2 decrypts
	if (command == 0)
		keyGen(argv[2]);  // keyFile
	else
		fileControl(argv[2], argv[3], argv[4], command);	//keyFile, FileIn, FileOut, command
	return 0;
}

/*
Description: Randomly generates and stores alpha and beta values. Tha alpha value is randomly drawn from the set: {1,3,5,7,9,11,15,17,19,21,23,25}. The beta value is randomly drawn from the range: [1..25]
Input: name of file that stores the keys
Outpt: alpha and beta values on subsequent lines of keyFile
*/
void keyGen (string keyFile)
{
	unsigned seed = time(NULL);
 	srand(seed); 
 	
 	// alpha can only be an odd integer between 0 and 26 and not equal to 13
 	int key[] = {1,3,5,7,9,11,15,17,19,21,23,25};
 	int alpha = key[rand() % 12];
 	int beta = rand() % 25 + 1;
 	
 	// write alpha and beta onto lines 1 and 2 of keyFile
 	fstream fout;
 	fileOpen(fout, keyFile, 'w');
	fout << alpha << endl << beta << endl;
	fout.close();	
}

/*
Description: Encrypts an upper case alphabetic character using the affine cipher
Input: upper case alphabetic character, valid alpha and beta values
Returns: encrypted version of ch
*/
char encrypt (char ch, int alpha, int beta)
{
	int pos = ch - 'A';
	pos = (alpha*pos + beta) % 26;
	ch = pos + 'A';
	return ch;
}

/*
Description: Decrypts an upper case alphabetic character using the affine cipher
Input: upper case alphabetic character, valid alpha and beta values. Dictionary of multiplicative inverse values mod 26
Returns: decrypted version of input character
*/
char decrypt (char ch, int alpha, int beta)
{
	int inverseAlpha = MI[alpha];
	int pos = ch - 'A';
	pos = ((inverseAlpha * pos) - (inverseAlpha * beta) + (p*26)) % 26;
	ch = pos + 'A';
	return ch;
}

/*
Description: invokes fileOpen (../B-Files/7-openFileError.cpp in my GitHub repo) on all files. Close all files. Reads key file. Reads the input file and either invokes encrypt or decrypt. If the action is encrypt, alphabetic characters are transformed to upper case. Writes the result of encrypt or decrypt to the output file.
Input: names of key file, input file and output file. mode value of 1 or 2
Output: writes to the output file
*/
void fileControl (string keyFile, string fileIn, string fileOut, int mode)
{
	// Reads alpha and beta from keyFile
	fstream finK;
	fileOpen(finK, keyFile, 'r');
	int alpha, beta;
	finK >> alpha;
	finK >> beta;	
	finK.close();
	
	fstream fin;
	fstream fout;	
	fileOpen(fin, fileIn, 'r');		// Plain text if encrypt or Cipher text if decrypt
	fileOpen(fout, fileOut, 'w');	// Cipher text if encrypt or Decrypt text if decrypt
	
	while(fin.peek() != EOF)
 	{
 		char ch = fin.get();
 		if(isalpha(ch))
 		{
 			ch = toupper(ch);
 			if (mode == 1)			// if the command is to encrypt
 				fout.put(encrypt(ch, alpha, beta));
 			else if (mode == 2)		// if the command is to decrypt
 				fout.put(decrypt(ch, alpha, beta));
   		}
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
