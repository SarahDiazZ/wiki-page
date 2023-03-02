# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

# Create mock backend in file to test.

class Backend:

    def __init__(self):
        self.password_bucket = "usersandpasswords"
        self.content_bucket = "awesomewikicontent"
        self.storage_client = storage.Client()
        
    def get_wiki_page(self, name):
        bucket = self.storage_client.bucket(self.content_bucket)
        blob = bucket.get_blob(name)
        return blob.download_to_file()

    def get_all_page_names(self):
        page_names = []
        blobs = self.storage_client.list_blobs(self.content_bucket)
        for blob in blobs:
            page_names.append(blob.name)
        return page_names

    def upload(self, name, file):
        bucket = self.storage_client.bucket(self.content_bucket)
        blob = bucket.blob(name)
        if blob.exists():
            return False
        else:
            blob.upload_from_file(file)
            return True

    def sign_up(self, username, password):
        bucket = self.storage_client.bucket(self.password_bucket)
        blob = bucket.blob(username)
        if blob.exists():
            return False
        else:
            with blob.open("w") as b:
                b.write(password)
            return True

    def sign_in(self, username, password):
        bucket = self.storage_client.bucket(self.password_bucket)
        blob = bucket.get_blob(username)
        if not blob:
            return False
        else:
            with blob.open("r") as b:
                if b.read() == password:
                    return True
                return False

    def get_image(self, name):
        bucket = self.storage_client.bucket(self.content_bucket)
        blob = bucket.get_blob(name)
        return blob.download_to_file()
