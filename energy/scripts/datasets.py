import os
from pathlib import Path
from authentication import ws
from azureml.core import Dataset
from azureml.data.dataset_factory import DataType

def data_filepaths(data_folder='./input-data'):
    """Get full paths to discrete data files"""
    full_filepaths = []
    absolute_path = Path(data_folder).absolute()
    data_files = os.listdir(data_folder)
    for file in data_files:
        file_with_path = str(absolute_path) + '/' + str(file)
        full_filepaths.append(file_with_path)
    return full_filepaths


def register_dataset(dataset=None, workspace=None, name=None, desc=None,tags=None):
    """Register datasets"""
    try:
        dataset = dataset.register(
                workspace=workspace, 
                name=name, 
                description=desc, 
                tags=tags,
                create_new_version=True
                )
        print(f" Dataset registration successful for {name}")
    except Exception as e:
        print(f" Exception in registering dataset. Error is {e}")


def main():
    """Main operational flow"""

    # Set target locations
    local_data_folder = './../input-data'
    target_def_blob_store_path = '/blob-input-data/'

    # Get input data files from local
    data_file_paths = data_filepaths(data_folder = local_data_folder)

    # Get the default blob store
    def_blob_store = ws.get_default_datastore()

    # Upload files to blob store
    def_blob_store.upload_files(
            files=data_file_paths, 
            target_path=target_def_blob_store_path,
            overwrite=True,
            show_progress=True
            )
    
    ## Parquet option
    #datastore_paths = [(def_blob_store, str(target_def_blob_store_path + 'energy-train.parquet'))]
    #fd= Dataset.Tabular.from_parquet_files(path=datastore_paths)

    # CSV option
    datastore_paths = [(def_blob_store, str(target_def_blob_store_path + 'energy-train-processed.csv'))]
    fd= Dataset.Tabular.from_delimited_files(path=datastore_paths, set_column_types={
        'Date':DataType.to_datetime(formats='%Y-%m-%dT%H:%M:%S'),
        #'Date':DataType.to_datetime(),
        'TZ':DataType.to_string(),
        'Code':DataType.to_string(),
        'Load':DataType.to_float()
        })


    # Register the dataset
    register_dataset(dataset=fd, workspace=ws, name='energy-train-processed')

if __name__ == "__main__":
    main()
