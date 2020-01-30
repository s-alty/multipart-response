import os

from mp_response import MultipartFileContent, MultipartResponse


def serve_multiple_files(request):
    # return the contents of a directory in a single http response
    parts = []
    entries = (f for f in os.scandir('.') if f.is_file())
    for i, entry in enumerate(entries):
        with open(entry.path, 'rb') as handle:
            content = handle.read()

        parts.append(
            MultipartFileContent(
                content,
                'field_{}'.format(i),
                file_name=entry.name
            )
        )
    return MultipartResponse(parts)
