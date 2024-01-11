import logging
import errno
from google.cloud import storage


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client=storage.Client() 
    with open(local_file, 'rb') as f:
        bucket = client.bucket(bucket)
        blob = bucket.blob(object_name)
        logging.info(f"Starting upload of {local_file} to {object_name}") 
        if blob.exists():
            blob.upload_from_file(f, rewind=True) 
        else:
            blob.upload_from_file(f)
        logging.info(f"Finished upload of {local_file} to {object_name}")
    return blob.public_url