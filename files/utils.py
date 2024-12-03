from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict
from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
import csv
import os
import pandas as pd
import io


async def get_csv_file_validations(uploaded_csv: UploadFile) -> Dict:

    dataframe = pd.read_csv(uploaded_csv.file)


    validations = {
        "empty_values": [],
        "incorrect_types": [],
        "duplicate_rows": []
    }

    empty_values = dataframe.isnull().sum()
    for column, count in empty_values.items():
        if count > 0:
            validations["empty_values"].append({"column": column, "empty_count": count})    


    duplicated_rows = dataframe[dataframe.duplicated()]
    if not duplicated_rows.empty:
        validations["duplicate_rows"] = duplicated_rows.to_dict(orient="records")            

    print(validations)

    return validations





async def serialize_csv_data(uploaded_csv: UploadFile) -> Dict:
    
    dataframe = pd.read_csv(uploaded_csv.file)

    print(dataframe)
    
    csv_data = {"data": dataframe.to_dict(orient="records")}

    pprint(csv_data)

    
    # contents = uploaded_csv.file.read()
    # # decoded_contents = contents.decode("utf-8")
    # print("content: ", contents)

    # csv_file = io.StringIO(decoded_contents)
    
    # reader = csv.DictReader(csv_file)
    
    

    return csv_data





