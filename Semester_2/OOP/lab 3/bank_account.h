#include <iostream>
#include <string>
#include <cmath>

class BankAccount {
  private:
    std::string holderName;
    int number;
    double balance;

  public:
    BankAccount();
    BankAccount(std::string holderNameValue, int numberValue, double balanceValue);
    
    std::string getHolderName();
    int getNumber();
    double getBalance();

    void setHolderName(std::string holderNameValue);
    void setNumber(int numberValue);
    void setBalance(double balanceValue);

    static void depositFunds(BankAccount& account, double funds);
    static void withdrawFunds(BankAccount& account, double funds);

    friend std::ostream& operator<<(std::ostream& os, const BankAccount& point); 
    friend std::istream& operator>>(std::istream& is, BankAccount& point);
};


