from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
import os


class CommunityPhotoAlbum(object):

    def get_photos_url(self, name):
        raise NotImplementedError("Subclass")


class FileSystemPhotoAlbum(CommunityPhotoAlbum):

    def get_photos_url(self, name):
        b = os.path.join(settings.BASE_DIR, "static", "img", "community_photos", name)

        if not os.path.exists(b):
            return list()

        results = list()
        for filename in os.listdir(b):
            results.append(static("img/community_photos/%s/%s" % (name, filename)))
        return results


class SocialNetworkPhotoAlbum(CommunityPhotoAlbum):
    def get_photos_url(self, name):
        """
        Get the photos URLs from an external service like Flickr, facebook, Dropbox.
        """
        pass