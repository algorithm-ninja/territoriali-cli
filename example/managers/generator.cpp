#include <random>
#include <iostream>
#include <cassert>
#include <string>
#include <cstdint>

using namespace std;

int main(int argc, char* argv[])
{
    assert(argc == 3);
    auto seed = atoll(argv[1]);
    auto param = atoll(argv[2]);
    const auto n = 50;
    mt19937_64 r(seed);
    cout << to_string(n) << endl;
    for(auto i = 0; i < n; i++)
    {
        switch(i % 13)
        {
            case 4:
                cout << UINT64_MAX - r() % 10 << " " << UINT64_MAX - r() % 10 << endl;
                break;
            case 9:
                cout << r() << " " << r() << endl;
                break;
            default:
                cout << r() % (1 << 31) << " " << r() % (1 << 31) << endl;
                break;
        }
    }
    return 0;
}
