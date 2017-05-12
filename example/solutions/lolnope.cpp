#include <iostream>
#include <random>

using namespace std;

int main()
{
    mt19937 r(42);
    int t;
    cin >> t;
    for(int caso = 0; caso < t; caso++)
    {
        uint64_t a, b;
        cin >> a >> b;
        if(r() % 10 == 0)
            continue;
        cout << "Case #" << caso << ": ";
        if(r() % 3 == 0)
            cout << "ayylmao";
        else
            cout << a + b;
        cout << endl;
    }
    return 0;
}
