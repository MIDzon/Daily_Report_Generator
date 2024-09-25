Batch creator 09/24/2024
How to use the tool for tools
1. Double click on Daily_Report_Generator.exe
2. input the date in MM-DD-YYYYY format
	if the month or day is a single digit, add a 0 (ex. January 1, 2024 will be 01-01-2024) if not do not add a 0 (ex. November 12, 2024 will be 11-12-2024)
3. The new batch file will be named "[Strand #]_reports.bat" and "Relabel [#]_reports.bat"

There are 3 controlled files need to be in the same location as the Daily_Report_Generator.exe
	Batch_File_Loc - Location for where the batch file will be moved once created
	Looped_List - Contains a list off all the reports that we want to pull for the strands ONLY
	Looped_List_Not - Contains a list off all the reports that we want to pull for the relabel ONLY
-All 3 controlled files are editable
	