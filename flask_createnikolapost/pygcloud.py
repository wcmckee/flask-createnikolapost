#!/usr/bin/env python
# coding: utf-8

# In[1]:


from google.cloud import storage
import os
import subprocess


# In[2]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/wcmckee/test.json"


# In[ ]:


storage_client = storage.Client()


# In[ ]:


def createbucket(nameofbucket):
    bucket = storage_client.create_bucket(nameofbucket)
    return('Bucket {} created.'.format(bucket.name))


# In[ ]:


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


# In[ ]:


def uploadstatic(bucket, url):
    for path, subdirs, files in os.walk(url):
        for name in files:
            filedir = (os.path.join(path, name))
            upload_blob(bucket, filedir, filedir.replace(url, ''))
            print(name)
            #make_blob_public(bucket, filedir.replace(url, ''))


# In[1]:


def makebucketpublic(bucket): 
    subprocess.run("gsutil iam ch allUsers:objectViewer gs://{}".format(bucket), shell=True)


# In[2]:


def makebucketsync(bucket, url): 
    subprocess.run("gsutil rsync -r {} gs://{}".format(url, bucket), shell=True)


# In[ ]:





# In[ ]:


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)


# In[ ]:


def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print('Blob {} is publicly accessible at {}'.format(
        blob.name, blob.public_url))

