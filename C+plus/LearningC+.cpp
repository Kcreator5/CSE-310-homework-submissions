#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <limits>

using namespace std;

enum Move { Rock = 1, Paper, Scissors, Lizard, Spock, Quit };

struct RoundResult {
    int player;
    int computer;
    string outcome;
};

class RPSGame {
public:
    RPSGame() {
        srand(static_cast<unsigned>(time(nullptr)));
    }

    void run() {
        clearScreen();
        printIntro();
        while (true) {
            int player = getPlayerChoice();
            if (player == Quit) break;

            int computer = getComputerChoice();
            string result = getOutcome(player, computer);
            history.push_back({player, computer, result});

            printRound(player, computer, result);
            waitForKey();
            clearScreen();
            printIntro();
        }
        printSummary();
    }

private:
    vector<RoundResult> history;

    void clearScreen() const {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
    }

    void waitForKey() const {
        cout << "Press Enter to continue...";
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cin.get();
    }

    void printIntro() const {
        cout << "=== Rock Paper Scissors Lizard Spock ===\n";
        cout << "1. Rock\n2. Paper\n3. Scissors\n4. Lizard\n5. Spock\n6. Quit\n";
    }

    int getPlayerChoice() const {
        int choice;
        while (true) {
            cout << "Enter your choice: ";
            cin >> choice;
            if (choice >= Rock && choice <= Quit) {
                return choice;
            }
            cout << "What even is that choice. Try again.\n";
        }
    }

    int getComputerChoice() const {
        return rand() % 5 + 1;
    }

    string moveName(int move) const {
        switch (move) {
            case Rock: return "Rock";
            case Paper: return "Paper";
            case Scissors: return "Scissors";
            case Lizard: return "Lizard";
            case Spock: return "Spock";
            default: return "Unknown";
        }
    }

    string getOutcome(int player, int computer) const {
        if (player == computer) return "Tie";
        if ((player == Rock && (computer == Scissors || computer == Lizard)) ||
            (player == Paper && (computer == Rock || computer == Spock)) ||
            (player == Scissors && (computer == Paper || computer == Lizard)) ||
            (player == Lizard && (computer == Paper || computer == Spock)) ||
            (player == Spock && (computer == Rock || computer == Scissors))) {
            return "Win";
        }
        return "Lose";
    }

    void printRound(int player, int computer, const string& outcome) const {
        cout << "You chose: " << moveName(player) << "\n";
        cout << "Computer chose: " << moveName(computer) << "\n";
        cout << "Result: You " << outcome << "!\n\n";
    }

    void printSummary() const {
        int wins = 0, losses = 0, ties = 0;
        for (auto& r : history) {
            if (r.outcome == "Win") wins++;
            else if (r.outcome == "Lose") losses++;
            else ties++;
        }
        cout << "the game is over. Rounds played: " << history.size() << "\n";
        cout << "rounds you've won: " << wins << ", rounds you've lost: " << losses << ", Ties: " << ties << "\n";
    }
};

int main() {
    RPSGame game;
    game.run();
    return 0;
}