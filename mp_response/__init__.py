import random
import string

from django.http import HttpResponse

# https://tools.ietf.org/html/rfc7578

def _boundary_line(boundary):
    return ('--' + boundary).encode('utf-8')

def _disposition_line(field_name, file_name):
    l = 'Content-Disposition: form-data; name="{}"'.format(field_name)
    if file_name is not None:
        l += '; filename="{}"'.format(file_name)
    return l.encode('utf-8')

def _content_type_line(content_type, charset):
    l = 'Content-Type: {}'.format(content_type)
    if charset is not None:
        l += '; charset={}'.format(charset)
    return l.encode('utf-8')


class MultipartFileContent(object):
    def __init__(self, content, field_name, file_name=None, content_type='application/octet-stream', charset=None):
        self.content = content
        self.field_name = field_name
        self.file_name = file_name
        self.content_type = content_type
        self.charset = charset

    def encode(self, boundary):
        return b'\r\n'.join([
            _boundary_line(boundary),
            _disposition_line(self.field_name, self.file_name),
            _content_type_line(self.content_type, self.charset),
            b'', # blank line before content
            self.content,
            b'' # blank line after content
        ])


class MultipartResponse(HttpResponse):
    def __init__(self, parts, boundary=None, **kwargs):
        if boundary is None:
            # choose a random bounary
            boundary = ''.join(random.choice(string.digits) for _ in range(32))

        content_type = 'multipart/form-data; boundary="{}"'.format(boundary)
        kwargs['content_type'] = content_type

        content = b''.join(p.encode(boundary) for p in parts)
        # final boundary
        content += '--{}--'.format(boundary).encode('utf-8')
        super().__init__(content, **kwargs)
