# -*- coding: utf-8 -*-

# Reference: https://gree2.github.io/python/2016/03/30/python-multipart-form-post-data

import httplib
import os.path

def post_multipart(host, port, username,file_place, filename):
     """
     Post fields and files to an http host as multipart/form-data.
     fields is a sequence of (name, value) elements for regular form fields.
     files is a sequence of (name, filename, value) elements for data to be uploaded as files
     Return the server's response page.
     """

     file_content = open(filename, 'rb').read()
     file_base_name = os.path.basename(filename)

     content_type, body = encode_multipart_formdata(file_base_name, file_content)
     h = httplib.HTTP(host, port=port)
     h.putrequest('POST', '/put_file/'+username + file_place)
     h.putheader('content-type', content_type)
     h.putheader('content-length', str(len(body)))
     h.endheaders()
     h.send(body)
     errcode, errmsg, headers = h.getreply()
     return h.file.read()

def encode_multipart_formdata(file_base_name, file_content):
     """
     fields is a sequence of (name, value) elements for regular form fields.
     files is a sequence of (name, filename, value) elements for data to be uploaded as files
     Return (content_type, body) ready for httplib.HTTP instance
     """
     BOUNDARY = '----------fhgfhfhfrrht44343987tuf'
     CRLF = '\r\n'
     L = []

     L.append('--' + BOUNDARY)
     L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', file_base_name.encode('ascii')))
     L.append('Content-Type: application/octet-stream')
     L.append('')
     L.append(file_content)
     L.append('--' + BOUNDARY + '--')
     L.append('')
     body = CRLF.join(L)
     content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
     return content_type, body

if __name__ == '__main__':
    post_multipart("localhost", 5000, "yuval","/root/yuval", "c:\\temp\\flask1.py")
