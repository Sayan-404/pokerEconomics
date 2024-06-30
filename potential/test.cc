#include <iostream>
#include <vector>
#include <algorithm>

// Function to generate combinations
std::vector<std::vector<std::string>> generateCombinations(const std::vector<std::string> &elements, int r)
{
    std::vector<std::vector<std::string>> combinations;

    if (r > elements.size() || r <= 0)
        return combinations;

    std::vector<bool> v(elements.size());
    std::fill(v.begin(), v.begin() + r, true);

    do
    {
        std::vector<std::string> combination;
        for (size_t i = 0; i < elements.size(); ++i)
        {
            if (v[i])
                combination.push_back(elements[i]);
        }
        combinations.push_back(combination);
    } while (std::prev_permutation(v.begin(), v.end()));

    return combinations;
}

std::vector<std::string> create_deck()
{
    std::vector<std::string> suits = {"h", "d", "c", "s"};
    std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
    std::vector<std::string> deck;
    for (const auto &suit : suits)
    {
        for (const auto &rank : ranks)
        {
            deck.push_back(rank + suit);
        }
    }
    return deck;
}

int main()
{
    std::vector<std::string> elements = create_deck();
    int r = 5;

    std::vector<std::vector<std::string>> combos = generateCombinations(elements, r);

    // Print combinations
    for (const auto &combo : combos)
    {
        std::cout << "[ ";
        for (const auto &item : combo)
        {
            std::cout << item << " ";
        }
        std::cout << "]\n";
    }

    return 0;
}
