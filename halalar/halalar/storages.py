from __future__ import absolute_import

from storages.backends.s3boto import S3BotoStorage

MediaS3BotoStorage = lambda: S3BotoStorage(bucket='halalar-media')
StaticS3BotoStorage  = lambda: S3BotoStorage(bucket='halalar')