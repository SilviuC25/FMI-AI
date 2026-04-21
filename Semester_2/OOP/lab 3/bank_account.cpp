#include "bank_account.h"
#include <iostream>
#include <iomanip>

BankAccount::BankAccount() : holderName{""}, number{0}, balance(0.0f) {}

BankAccount::BankAccount(std::string holderNameValue, int numberValue, double balanceValue) {
  holderName = holderNameValue;
  number = numberValue;
  balance = balanceValue;
}

std::string BankAccount::getHolderName() {
  return holderName;
}

int BankAccount::getNumber() {
  return number;
}

double BankAccount::getBalance() {
  return balance;
}

void BankAccount::setHolderName(std::string holderNameValue) {
  holderName = holderNameValue;
}

void BankAccount::setNumber(int numberValue) {
  number = numberValue;
}

void BankAccount::setBalance(double balanceValue) {
  balance = balanceValue;
}

void BankAccount::depositFunds(BankAccount& account, double funds) {
  account.balance += funds;
}

void BankAccount::withdrawFunds(BankAccount& account, double funds) {
  if (account.balance < funds) {
    std::cout << "Can't withdraw funds greater than account's balance";
    return;
  }
  account.balance -= funds;
} 

std::ostream& operator<<(std::ostream& os, const BankAccount& account) { 
  os << "Holder's name is: " << account.holderName << "\nThe account's number is: " << account.number <<
    "\nThe balance is: " << std::setprecision(2) << std::fixed << account.balance << "\n"; 
  return os; 
} 

std::istream& operator>>(std::istream& is, BankAccount& account) { 
  is >> account.holderName >> account.number >> account.balance;
  return is; 
} 
