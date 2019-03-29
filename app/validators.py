import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_if_is_pdf_file(value):
    """
    Only checks if the extension is .pdf
    """
    if not (os.path.splitext(value.name)[1] == ".pdf"):
        raise ValidationError(_("Please upload a PDF file"))
