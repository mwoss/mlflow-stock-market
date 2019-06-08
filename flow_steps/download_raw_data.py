import click
import csv
import mlflow
import requests
import tempfile
from os import path

QUANLD_API = "https://www.quandl.com/api/v3/datasets"


@click.command(help="Downloads the stock market dataset for given company. Saves it as an mlflow artifact")
@click.option("--company-name", type=str)
@click.option("--dataset-name", type=str)
def download_csv(company_name: str, dateset_name: str):
    dataset_url = f"{QUANLD_API}/{company_name}/{dateset_name}"

    with mlflow.start_run() as mlrun:
        local_dir = tempfile.mkdtemp()
        local_filename = path.join(local_dir, "dataset-market.csv")
        print(f"Downloading {dataset_url} to {local_filename}")

        dataset = requests.get(dataset_url)
        decoded_content = dataset.content.decode("utf-8").splitlines()

        with open(local_filename, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            for line in decoded_content:
                columns = line.split(",")
                writer.writerow(columns)
        
        print(f"Uploading stock market data: {local_filename}")
        mlflow.log_artifact(local_filename, "dataset-stock-dir")


if __name__ == '__main__':
    download_csv()
    