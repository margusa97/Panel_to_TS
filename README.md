# Panel_to_TS
I created this repository for a Research project at Bocconi Univeristy to transform panel data into time-series data.
These data refer to stocks in different kind of markets.
This repository is composed of three scripts:
- ReadWrite.py: it contains the ReadWrite object, which has method useful to extract data out from a single Excel sheet and paste them correctly using pandas and numpy libraries
- Execution.py: this scripts basically iterates to a series of Excel Sheets and creates new Excel files
- Debugger.py: script which has important debugging tools used to detect problem for a specific Excel sheet
