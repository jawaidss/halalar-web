import boto
from datetime import datetime
import os
import tempfile

from django.conf import settings

def run():
    now = datetime.now()
    basename = now.strftime('%F-%H-%M-%S')
    filename = os.path.join(tempfile.gettempdir(), basename)

    os.system('pg_dump -Fc -U %s %s > %s' % (settings.DATABASES['default']['USER'],
                                             settings.DATABASES['default']['NAME'],
                                             filename))

    connection = boto.connect_s3()
    bucket = connection.get_bucket(settings.AWS_BACKUP_BUCKET_NAME)
    key = bucket.new_key(basename)
    key.set_contents_from_filename(filename)

    print filename, '-->', 's3://%s/%s' % (bucket.name, key.key)