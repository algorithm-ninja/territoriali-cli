#include <iostream>

using namespace std;

int main()
{
    int t;
    cin >> t;
    for(int caso = 0; caso < t; caso++)
    {
        uint64_t a, b;
        cin >> a >> b;
        cout << "Case #" << caso << ": " << a + b << endl;
    }
    return 0;
}
