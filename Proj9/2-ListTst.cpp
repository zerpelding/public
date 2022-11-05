#include <iostream>
using namespace std;

#include "2-List.h"

int main()
{
 	List lst;
 	List* lst1 = new List;

 	cout << "Test Dynamic Insert and Print" << endl;
 	cout << "Correct if out is 4, 3, 2, 1, 0 on subsequent lines" << endl;
/*
 	for (int i = 0; i < 5; i++)
  		lst1->PutItemH(i);
   	lst1->Print();
*/

	
//	cout << "Item at the head: " << lst1->GetItemH() << endl;

/*
	lst1->DeleteItemH();
	lst1->Print();
*/
	
//	cout << "Length: " << lst1->GetLength() << endl;
	
//	cout << "Number of found items: " << lst1->Find(2) << endl;
	
//	cout << "Number of deleted items: " << lst1->DeleteItem(2) << endl;
//	lst1->Print();

/*	
	if (lst1->IsEmpty())
		cout << "Empty!" << endl;
	else 
		cout << "Not empty!" << endl;
*/

 	delete lst1; 
 	cout << endl;
 	
 	return 0;
}
