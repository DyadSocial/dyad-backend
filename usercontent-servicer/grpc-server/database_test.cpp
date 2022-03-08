#include <iostream>
#include <database_helper.hpp>

int main(void) {
  DatabaseHelper *db_h = DatabaseHelper::GetInstance();
  db_h->StoreProfileImage("vncp", "helloworlld");
  std::cout << db_h->GetProfileImage("vncp") << "\n";
}