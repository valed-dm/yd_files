"""Yafiles models"""

from django.db import models


class File(models.Model):
    """
       Represents a file with metadata and a public link.

       Attributes:
           type (str): Type of the file (e.g., 'image', 'document').
           mime_type (str): MIME type of the file.
           name (str): Name of the file.
           path (str): Path to the file within the public link.
           file_url (str): URL where the file can be downloaded.
           public_link (str): Public link to the directory containing the file.
           size (int): Size of the file in bytes.
           created (datetime): Timestamp when the file was created.
           modified (datetime): Timestamp when the file was last modified.
       """
    type = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    file_url = models.URLField(max_length=1024)
    public_link = models.URLField(max_length=255)
    size = models.BigIntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "public_link"],
                name="unique_name_public_link"),
        ]

    def __str__(self) -> str:
        return f"{self.name!r}"


class Preview(models.Model):
    """
       Represents a preview image for a file.

       Attributes:
           file (File): The file that this preview belongs to.
           size_name (str): Name or size of the preview (e.g., 'small', 'medium').
           preview_url (str): URL where the preview image can be viewed.
       """
    file = models.ForeignKey(File, related_name="previews", on_delete=models.CASCADE)
    size_name = models.CharField(max_length=10)
    preview_url = models.URLField(max_length=1024)

    def __str__(self) -> str:
        return f"{self.size_name!r}"
