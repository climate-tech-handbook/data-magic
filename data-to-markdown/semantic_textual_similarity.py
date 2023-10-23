"""
Semantic Similarity between Company descriptions and Drawdown Solutions

Inputs are master company dataset and master drawdown solution csv files.

Every time there is a new company in the master dataset, this script needs to be run manually. After a succesful run it creates, two files

- data/matched_company_with_drawdown_solution_cleaned.csv
- data/sorted.json
"""
# TODO: Clean data with nan

import json
import pandas as pd
import requests
import streamlit as st

from pathlib import Path
from sentence_transformers import SentenceTransformer, util

from utils import capitalize_name, check_and_add_missing_https

model = SentenceTransformer("all-MiniLM-L6-v2")


def match_company_to_a_drawdown_solution(file1_path, file2_path):
    """
    file1 csv must be company data
    file2 csv must be drawdown solutions
    """

    # Load CSV data into pandas DataFrames
    df1 = pd.read_csv(file1_path, encoding="utf-8")
    df2 = pd.read_csv(file2_path, encoding="utf-8")

    # Select columns containing sentences for semantic similarity
    column1 = "Description"  # company description
    column2 = "Definition"  # drawdown definition
    # Columns not used for embeddings
    column3 = "Name"
    column4 = "Drawdown Solution"  # groundtruth
    column5 = "Website"
    column6 = "Drawdown Solution"  # for mapping

    # Drop rows with any missing values
    df1_cleaned = df1.dropna(subset=[column1])

    # Summary
    print("Summary")
    print("----------------------------------------")
    print("Total Companies:", len(df1))
    print("Number of companies missing description:", len(df1) - len(df1_cleaned))
    print("Processing {} companies......".format(len(df1_cleaned)))
    print("----------------------------------------")

    # Get sentences from both DataFrames
    # embedded
    companies_description = df1_cleaned[column1].astype(str).tolist()
    drawdown_descriptions = df2[column2].astype(str).tolist()
    # non embedded
    company_names = df1_cleaned[column3].astype(str).tolist()
    groudtruth_drawdown_solutions = df1_cleaned[column4].astype(str).tolist()
    company_website = df1_cleaned[column5].astype(str).tolist()
    drawdown_solutions = df2[column6].astype(str).tolist()

    # Compute embedding for both lists
    embeddings1 = model.encode(companies_description, convert_to_tensor=True)
    embeddings2 = model.encode(drawdown_descriptions, convert_to_tensor=True)

    # Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    # Output the drawdown solution with highest score for a company
    # saving it in .csv
    # using brute force

    matched_csv_column_names = [
        "Company",
        "Predicted Drawdown Solution",
        "Groundtruth Drawdown Solution",
        "Probability Score",
        "Company Description",
        "Drawdown definition",
        "Website",
    ]

    data = []
    for i in range(len(companies_description)):
        max_index, max_score = max(enumerate(cosine_scores[i][:]), key=lambda x: x[1])
        # print("{} \t\t {} \t\t {} \t\t Score: {:.4f}".format(company_names[i], drawdown_solutions[max_index], drawdown_descriptions[max_index], max_score))
        # csv
        data.append(
            [
                capitalize_name(company_names[i]),
                drawdown_solutions[max_index],
                groudtruth_drawdown_solutions[i],
                max_score,
                companies_description[i],
                drawdown_descriptions[max_index],
                check_and_add_missing_https(company_website[i]),
            ]
        )
    df = pd.DataFrame(data)
    df.columns = matched_csv_column_names
    # Sort the DataFrame based on the specified column
    sorted_df = df.sort_values(by="Predicted Drawdown Solution")
    sorted_df.to_csv(
        "data/matched_company_with_drawdown_solution_cleaned.csv", index=None
    )


def sort_companies_based_on_drawdown_solutions(csv_path):
    """
    Takes the matched csv and gives a list of companies for each drawdown solution
    input: matched csv
    returns: {drawdown_solution:[companies],{},.... }
    """

    column = "Predicted Drawdown Solution"
    # Load CSV data into pandas DataFrames
    df = pd.read_csv(csv_path, encoding="utf-8")

    # creating a dict and writing to a json file
    sorted_dict = {}
    for i, key in enumerate(df[column]):
        company_name = df["Company"][i]
        company_website = df["Website"][i]
        info = {"name": company_name, "website": company_website}
        if key in sorted_dict:
            sorted_dict[key].append(info)
        else:
            sorted_dict[key] = [info]
    with open("data/sorted.json", "w") as json_file:
        json.dump(sorted_dict, json_file, indent=4)


def run_streamlit(json_path, csv_path):
    st.title("Companies based on Drawdown Solution")
    with open(json_path) as json_file:
        data = json.load(json_file)
    drawdown_solutions = data.keys()

    drawdown_selected = st.selectbox(
        "Pick a Drawdown solution", options=drawdown_solutions
    )
    if drawdown_selected:
        st.write("Companies:", data[drawdown_selected])

    st.title("Matched Climate Companies to a Drawdown Solution")
    st.dataframe(
        pd.read_csv(csv_path),
        width=1200,
        height=700,
        hide_index=True,
    )


if __name__ == "__main__":
    matched_csv_path = Path("data/matched_company_with_drawdown_solution_cleaned.csv")
    json_path = Path("data/sorted.json")

    if matched_csv_path.exists():
        run_streamlit(json_path, matched_csv_path)

    else:
        # Load CSV files
        file1_path = "data/Org data - Master List - MASTER.csv"
        file2_path = "data/Org data - Master List - Drawdown Solutions.csv"

        match_company_to_a_drawdown_solution(file1_path, file2_path)
        sort_companies_based_on_drawdown_solutions(matched_csv_path)
        run_streamlit(json_path, matched_csv_path)
