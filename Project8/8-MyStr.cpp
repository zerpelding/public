#include <iostream>
using namespace std;

#include "8-MyStr.h"
#include <cstring>

   /*
   Desc: Constructor for MyString. 
   Input:  strIn is a null-terminated array of characters
   Output: Instance of MyString is created 
   */ 
MyString::MyString(char const* strIn)
{
	length = strlen(strIn);  //strlen function
	str = new char[length + 1];
 	strcpy(str, strIn); //strlen function
}

  /*
   Desc: Destructor for MyString 
   Invoked automatically when a static instance of MyString 
   goes out of scope. Invoked when a dynamic instance of MyString
   is deleted.  
   Pre: A instance of MyString exists 
   Post: Dynamically declared memory is returned to the heap 
   */ 
MyString::~MyString()
{
 	delete []str; 
}

   /*
   Desc: Displays the contents of MyString 
   Pre: None
   Post: Contents of MyString are displayed on the screen 
   */ 
void MyString::myDisplay()
{
 	cout << str << endl;
}

   /*
   Desc: Used to determine the length of the argument
   Pre:  An instance of MyString exists
   Post: Returns the number of characters, excluding the null character
         in pointed to by the argument 
   */
int MyString::myStrLen(char const* strIn)
{
 	int idx = 0;
 	while (strIn[idx] != '\0')
  		idx++;
 	return idx;
}

   /*
   Desc: Used to determine the length of MyString.str
   Pre:  An instance of MyString exists
   Post: Returns the number of characters, excluding the null character
         in MyString. 
   */
int MyString::myStrlen()
{ 	 
 	return myStrLen(str);
}

   /*
   Desc: Overwrites contents of MyString.str with what strIn points to 
   To clarify: nothing of str remains. strIn replaces it entirely
   Input: strIn is a null-terminated string: contents of strIn replaces MyString 
   */
void MyString::myStrcpy(char const* strIn)
{
	int len = myStrLen(strIn);
	char* temp = new char[len+1];
	for (int i = 0; i < len; i++)
		temp[i] = strIn[i];
	delete []str;
	str = temp;
	temp = NULL;
	length = len;
}

   /*
   Desc: Determines if MyString.str is equivalent to an input C-String 
   Pre:  An instance of MyString exists. strIn is a null-terminated
         string.
   Post: Returns true if the strings are equivalent, false otherwise 
   */
bool MyString::isEqual(char const* strIn)	
{
	bool equal = true;
	if (myStrLen(strIn) != length)
		equal = false;
	else	
		for(int i = 0; i < myStrLen(strIn); i++)
		{
			if (strIn[i] != str[i])
			{
				equal = false;
				break;
			}
		}
	return equal;
}

   /*
   Desc: Searches for a substring within MyString 
   Pre:  An instance of MyString exists
   Post: If strIn is a substring of MyString.str, returns
         the index of its starting positon, -1 otherwise
   */
int MyString::find(char const* strIn) 
{
	int find = -1;
	for (int i = 0; i < length; i++)
	{
		if (str[i] == strIn[0])
		{
			if (isSub(strIn, i))
			{
				find = i;
				break;
			}
		}
	}
	return find;
}

   /*
   Desc: Used in conjunction with the function, find. Loops through MyString starting
         with idx looking for strIn.
   pre: idx is the first character of MyString.str that matches the substring, strIn
   post: returns true if strIn is a substring of str, false otherwise. 
         Used by find()
   */ 
bool MyString::isSub(char const* strIn, int idx)
{
	bool sub = true;
	int current = 0;
	while(current < myStrLen(strIn))
	{
		if (str[idx] != strIn[current])
		{
			sub = false;
			break;
		}
		current++;
		idx++;
	}
	return sub;
}

   /*
   Desc: Concatenates strIn with MyString 
   Pre:  An instance of MyString exists. strIn is a null-terminated string
   Post: strIn is concatenated with MyString.str.  Ex.
         MyString.str is ABC. strIn is DEF.  MyString is still a null-terminated
	 string, but contains: ABCDEF. 
   */
void MyString::concat(char const* strIn) 
{
	int len = length + myStrLen(strIn);
	char* temp = new char [len + 1];
	for (int i = 0; i < length; i++)
		temp[i] = str[i];
	for (int j = length, k = 0; j < len + 1; j++, k++)
		temp[j] = strIn[k];
	delete []str;
	str = temp;
	temp = NULL;
	length = len;
}



