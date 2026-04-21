#include "bank_account.h"  
#include <iostream> 
using namespace std; 

int main(void) {
  BankAccount account1;
  cout << "Enter the account details:\n";
  cin >> account1;
  cout << "You entered:\n" << account1;
  BankAccount account2{ "Silviu", 1, 100 };
  BankAccount::depositFunds(account1, 1000);
  BankAccount::withdrawFunds(account2, 50);
  cout << account1.getBalance() << " " << account2.getBalance();
  return 0;
}