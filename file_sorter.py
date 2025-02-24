import pandas as pd
import os
import shutil
import time as timer

'''
Created by Jan Kyle Lewis T. Nolasco
'''

def search_file(file_name_kw, sort_file_df):
    filtered_df=sort_file_df[sort_file_df["File Name"].str.contains(file_name_kw)]
    filtered_df.reset_index(drop=True, inplace=True)
    n_found=len(filtered_df)
    if n_found==0:
        file_name=""
        found_flag=False
        multiple_flag=False
    elif n_found==1:
        file_name = filtered_df.loc[0, "File Name"]
        found_flag=True
        multiple_flag=False
    elif n_found>1:
        file_name = ""
        found_flag=True
        multiple_flag=True

    return file_name, found_flag, multiple_flag

def sort_files(sort_directory, file_db):
    #setup folder to find files in
    main_dir=os.getcwd()

    #create sort file DF
    sort_dir=os.path.join(main_dir, sort_directory)
    sort_file_list=[]

    for root, _, files in os.walk(sort_dir):

        for file_name in files:
            sort_file_list.append([file_name, os.path.join(root, file_name)])

    sort_file_df = pd.DataFrame(sort_file_list, columns=['File Name', 'Old Directory'])
    #sort_file_df.set_index('File Name', drop=True, inplace=True)

    #identify operation of each query
    file_db["Operation"]="Not Found"
    for index in file_db.index:
        #check if user identified a file name; uses this to search if given. Otherwise use Key Word instead
        if pd.isnull(file_db.loc[index, "File Name"]):
            file_name_kw = file_db.loc[index, "File Name Key Word"]
        else:
            file_name_kw = file_db.loc[index, "File Name"]
        try:
            file_name, found_flag, multiple_flag = search_file(file_name_kw, sort_file_df)
            if found_flag and not multiple_flag:
                file_db.loc[index, "Operation"]="Found"
                file_db.loc[index, "File Name"]=file_name
            elif found_flag and multiple_flag:
                file_db.loc[index, "Operation"] = "Multiple Files Found"
        except:
            pass

    #create output directory
    output_dir=os.path.join(main_dir, "output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    #copy files
    file_db=file_db.join(sort_file_df.set_index("File Name"), on="File Name")
    for index in file_db.index:
        if file_db.loc[index, "Operation"] == "Found":
            #create main folder
            new_dir=os.path.join(output_dir, file_db.loc[index, "Main Folder"])
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)

            shutil.copy(file_db.loc[index, "Old Directory"], os.path.join(new_dir, file_db.loc[index, "File Name"]))

    file_db.to_csv("sort_summary.csv", index=False)

def main():
    sort_directory="files_to_sort"
    dtype={
        "Main Folder": str,
        "File Name Key Word": str,
        "File Name": str
    }
    file_db=pd.read_csv("sort_list.csv", dtype=dtype)
    sort_files(sort_directory, file_db)

if __name__ == "__main__":
    start=timer.time()
    main()
    end=timer.time()
    total_time=(end-start)/60
    print(f"Elapsed Time: {total_time} mins")