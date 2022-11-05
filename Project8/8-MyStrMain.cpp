/*
Name: Paul De Palma
Class: CPSC 122, Section 1
Date Submitted: February 18, 2021
Assignment: N/A 
Description: Program illustrates using class MyString 
*/

#include "8-MyStr.h"
#include <iostream> 
using namespace std;


int main(int argc, char* argv[])
{
 	MyString str1(argv[1]);
 	MyString* str2 = new MyString(argv[1]);
	
 	//Test of myDisplay
 	cout << "*****Test myDisplay*****" << endl;
 	cout << "static test" << endl;

		////Testing myStrLen
// 	cout << "output should be the command line input" << endl;
// 	cout << str1.myStrlen() << endl;
 		
 		////Testing myDisplay
// 	str1.myDisplay();
 		
 		////Testing isEqual
// 	if(str1.isEqual("gonzaga"))
// 		cout << argv[1] << " is equal to gonzaga" << endl;
 		
 		////Testing find
// 	if (str1.find("zag") == -1)
// 		cout << "zag not found in " << argv[1] << endl;
// 	else if (str1.find("zag") != -1)
// 		cout << "zag found in " << argv[1] << " at index " << str1.find(argv[2]) << endl;

	 	////Testing myStrcpy
// 	str1.myStrcpy("dog");
// 	str1.myDisplay();
		
		////Testing concat
//	str1.concat("zag");
//	str1.myDisplay();
 	
 	cout << endl;
 	//End Test of myDisplay	


 	//Test of myStrlen
 	cout << "*****Test myStrlen*****" << endl;
 	cout << "dynamic test" << endl;
 	
 		////Testing myStrLen
// 	cout << "output should be length of command line input" << endl;
// 	cout << str2->myStrlen() << endl;
 	
 		////Testing myDisplay
 	str2->myDisplay();
 	
 		////Testing isEqual
// 	if(str2->isEqual("gonzaga"))
// 		cout << argv[1] << " is equal to gonzaga" << endl;
 		
 		////Testing find
// 	if (str2->find("zag") == -1)
// 		cout << "zag not found in " << argv[1] << endl;
// 	else if (str2->find("zag") != -1)
// 		cout << "zag found in " << argv[1] << " at index " << str2->find(argv[2]) << endl;

		////Testing myStrcpy
	str2->myStrcpy("cat");
 	str2->myDisplay();
 	cout << str2->myStrlen() << endl;
	
		////Testing concat
	str2->concat("zag");
	str2->myDisplay();
 	cout << str2->myStrlen() << endl;
 	
 	cout << endl;
 	//End Test of myStrlen


 	delete str2;
 	return 0;  
}
   
  
