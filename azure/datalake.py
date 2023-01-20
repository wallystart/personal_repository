import pandas as pd
from io import StringIO, BytesIO
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient

CONN_STR = ''
CONTAINER_NAME = ''


def upload_dataframe(path_file, df):
    """
    :param str path_file:
        test pathfile bla bla
    """
    blob = BlobClient.from_connection_string(conn_str=CONN_STR, container_name=CONTAINER_NAME, blob_name=path_file)

    # in memory
    buf = StringIO()
    df.to_csv(buf)

    # upload to lake
    return blob.upload_blob(buf.getvalue(), overwrite=True)


def upload_geodataframe(path_file, gdf):
    """
    :param str path_file:
        test pathfile bla bla
    """

    blob = BlobClient.from_connection_string(conn_str=CONN_STR, container_name=CONTAINER_NAME, blob_name=path_file)

    # in memory
    buf = BytesIO()
    gdf.to_file(buf, driver='GeoJSON')

    # upload to lake
    return blob.upload_blob(buf.getvalue(), overwrite=True)


def download_dataframe(path_file):
    container = ContainerClient.from_connection_string(conn_str=CONN_STR, container_name=CONTAINER_NAME)

    downloaded_blob = container.download_blob(path_file)

    return pd.read_csv(StringIO(downloaded_blob.content_as_text()))


def list_files(path, extension=".csv"):
    container = ContainerClient.from_connection_string(conn_str=CONN_STR, container_name=CONTAINER_NAME)

    generator = container.list_blobs(path)

    list_paths = []
    for blob in generator:
        if blob.name.find(extension) != -1:
            list_paths.append(blob.name)

    return list_paths


def download_dataframes_from(path):
    dfConcat = pd.DataFrame()
    for path_file in list_files(path, extension=".csv"):
        df = download_dataframe(path_file)
        dfConcat = pd.concat([dfConcat, df])

    return dfConcat


def upload_file(path_file_local, path_file_lake):
    blob_client = BlobClient.from_connection_string(conn_str=CONN_STR, container_name=CONTAINER_NAME, blob_name=path_file_lake)
    with open(path_file_local, 'rb') as fp:
        blob_client.upload_blob(fp, overwrite=True)

    # obtengo path
    path = blob_client.blob_name

    return path
