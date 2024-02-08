# Association Rule Mining

This project implements association rule mining using the ECLAT algorithm. It takes input data in the form of an Excel file and generates strong association rules based on the minimum support and confidence thresholds.

## Getting Started

### Prerequisites

- Python 3.7 or above
- Pandas library
- NumPy library

### Usage

1. Prepare your input data in an Excel file. The data should have a column containing transaction IDs and another column containing the items.

2. Update the `pathfile` variable in the code with the path to your Excel file.

3. Set the minimum support and confidence thresholds in the `min_sup` and `min_confidence` variables, respectively.

4. The code will generate the association rules and display them in the console. The strong association rules will be printed along with their confidence values. The lift values will also be calculated and displayed.

### Example

Suppose you have an Excel file named `data.xlsx` with the following data:

| TID | Item |
|-----|------|
| 1   | A, B |
| 2   | B, C |
| 3   | A, C |
| 4   | B, D |
| 5   | A, B, C |

You can run the code with a minimum support of 2 and a minimum confidence of 0.6. The code will generate the association rules and display them in the console.

## Acknowledgments

- The code is based on the ECLAT algorithm for association rule mining.
- Special thanks to the developers of the pandas and numpy libraries.
