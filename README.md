# file_sorter
## Input:
### All input variables can be found under main.
* sort_directory: Folder containing files to be sorted
* sort_list.csv: File containing information on how the files will be sorted. Each file must have a keyword to identify it and a folder it will be sorted into.
### sort_list
|Parameter|Description|
|---|---|
|Main Folder|Folder to group files together|
|File Name Key Word|Used to identify a file if the whole File Name is not known.|
|File Name|Used to identify a file|
## Output:
* output: Folder containing the sorted files. Within the folder, "Main Folders" can be found.
* sort_summary.csv: Summary of the sort operation. Identifies which files were properly sorted.
