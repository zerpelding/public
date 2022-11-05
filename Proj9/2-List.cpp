#include <iostream>
using namespace std;

#include "2-List.h"


   /*
   pre: None. This is the constructor function, invoked like this from the 
        the client program: 
        List lst;
	or
	List* lst1 = new List;
   post: an instance of List exists
   */ 
List::List()
{       
 	length = 0;
 	head = NULL;
}

   /*
   pre: An instance of List exists.  This is the destructor function, automatically
        invoked in the case of a static declaration, explcitly invoked, using the delete
        key word, in the case of a dynamic declaration.	
   post: All dynamically declared memory, i.e., the memory for all nodes, has been
        returned to the heap.   
   */
List::~List()
{
	while(head != NULL)
		DeleteItemH();
}

   /*
   pre: an instance of List exists
   post: node containing itemIn is at the head of the list 
   */
void List::PutItemH(const itemType itemIn)
{
	node* temp = new node;
	temp->next = head;
	temp->item = itemIn;
	head = temp;
	length++;
	temp = NULL;
} 
   
   /*
   pre: an instance of List exists and is not empty
   post: Returns the contents pointed to by the head of the list 
   */
itemType List::GetItemH() const
{
	itemType thing = head->item;
	return thing;
}
   /*
   pre: an instance of list exists and is not empty
   post: Node pointed to by head is deleted 
   */
void List::DeleteItemH()
{
	node* temp = head;
	head = head->next;
	delete temp;			
	temp = NULL;
	length--;
}

   /*
   pre: an instance of List exists
   post: returns true if list is empty, false otherwise
   */
bool List::IsEmpty() const
{
	bool empty = false;
	if(head == NULL)
		empty = true;
	return empty;
}

   /*
   pre: an instance of List exists
   post: returns length of the list 
   */
int List::GetLength() const
{
	return length;
}


   /*
   pre: an instance of list exists and is not empty
   post: contents of list nodes are displayed on subsequent lines, head to tail. 
   */
void List::Print() const
{
	node* cur = head;
	int i = 0;
	while(cur != NULL)
	{
		cout << cur->item << endl;
		cur = cur->next;
	}
}

   /*
   pre: an instance of List exists and is not empty
   post: returns the number of nodes in the list that stores target 
   */
int List::Find(const itemType target) const		
{
	int num = 0;
	node* temp = head;
	for (int i = 0; i < length; i++)
	{
		if (temp->item == target)
			num++;
		temp = temp->next;
	}
	return num;
}

   /*
   pre:  an instance of List exists and is not empty 
   post: deletes all nodes that store target.  Returns
         the number of nodes deleted 
   */
int List::DeleteItem(const itemType target) 			
{
	int num = 0;
	int total = Find(target);
	int len = length;
	
	while (head->item == target)
	{
		DeleteItemH();
		num++;
	}
	
	node* cur = head;
	int left = total - num;
	for (int i = 0; i < left; i++)
		num = Delete(target, num, cur);
	cur = NULL;
	
	return num;
}

	/*
	pre: an instance of List exists and is not empty
	post: deletes the next instance of the target. 
	Returns the new number of deleted items.
	*/
int List::Delete(const itemType target, int num, node* cur)
{
	while(cur->next->item != target)
		cur = cur->next;
	node* temp = cur->next;
	cur->next = temp->next;
	delete temp;
	num++;
	length--;
	temp = NULL;
	return num;
}

