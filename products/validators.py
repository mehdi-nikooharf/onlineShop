from pathlib import Path

import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileMimeValidator:
    messages = {
        "malicious_file": "File looks malicious. Allowed extensions are: '%(allowed_extensions)s'.",
        "not_supported": "File extension '%(extension)s' is not allowed. "
                         "Allowed extensions are: '%(allowed_extensions)s'."
    }
    code = 'invalid_extension'
    ext_cnt_mapping = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png'
    }

    def __init__(self, ):
        self.allowed_extensions = [allowed_extension.lower() for
            allowed_extension in self.ext_cnt_mapping.keys()]

    def __call__(self, data):
        extension = Path(data.name).suffix[1:].lower()
        content_type = magic.from_buffer(data.read(1024), mime=True)
        if extension not in self.allowed_extensions:
            raise ValidationError(
                self.messages['not_supported'],
                code=self.code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )
        if content_type != self.ext_cnt_mapping[extension]:
            raise ValidationError(
                self.messages['malicious_file'],
                code=self.code,
                params={
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_extensions == other.allowed_extensions and
            self.message == other.message and
            self.code == other.code
        )
