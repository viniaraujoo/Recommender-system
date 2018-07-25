# -*- coding: utf-8 -*-
import webapp2
import json
import os
from backend import get_top_5_movies_KNN, user_set, get_top_5_movies_SVD, get_top_5_neighbors,rmse_knn,rmse_svd

def read_file(path):
    path = os.path.dirname(os.path.realpath(__file__)) + '/frontend' + path
    file_stream = open(path, 'r')
    data = file_stream.read()
    file_stream.close()
    return data

def get_content_type(file):
    switch = {
        'js': 'application/javascript',
        'css': 'text/css',
        'html': 'text/html',
        'default': ''
    }

    file_type = file.split(".")[-1]
    return switch.get(file_type, switch['default'])


class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        """
        Método para gerênciar requisições GET.
        """
        uid = self.request.get('uid')
        response = {
            'result_knn': get_top_5_movies_KNN(uid),
            'result_svd': get_top_5_movies_SVD(uid),
            'neighbors': sorted(list(map(int, get_top_5_neighbors(uid)))),
            'rmse_knn':rmse_knn,
            'rmse_svd': rmse_svd
        }

        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(json.dumps(response))


class UsersIdHandler(webapp2.RequestHandler):
    def get(self):
        response = {
            'users_id': sorted(list(map(int, user_set)))
        }

        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(json.dumps(response))


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        path = '/index.html'
        data = read_file(path)

        self.response.headers['Content-Type'] = get_content_type(path.split('/')[-1])
        self.response.write(data)

class StaticsFilesHandler(webapp2.RequestHandler):
    def get(self):

        try:
            path = self.request.path
            data = read_file(path)

            self.response.headers['Content-Type'] = get_content_type(path.split('/')[-1])
            self.response.write(data)
        except:
            self.response.status = 404
        
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/api/results.*', ResultsHandler),
    ('/api/users', UsersIdHandler),
    ('/.*', StaticsFilesHandler)
], debug=True)


def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8081')


if __name__ == '__main__':
    main()