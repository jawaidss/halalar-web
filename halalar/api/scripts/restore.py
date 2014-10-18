import boto
import os
import tempfile

from django.conf import settings

def run():
    connection = boto.connect_s3()
    bucket = connection.get_bucket(settings.AWS_BACKUP_BUCKET_NAME)
    key = list(bucket.list())[-1]
    filename = os.path.join(tempfile.gettempdir(), key.key)
    key.get_contents_to_filename(filename)

    print 's3://%s/%s' % (bucket.name, key.key), '-->', filename

    os.system('dropdb -U postgres %s' % settings.DATABASES['default']['NAME'])
    os.system('pg_restore -C -U %s -d postgres %s' % (settings.DATABASES['default']['USER'],
                                                      filename))