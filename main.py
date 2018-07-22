# -*- coding: utf-8 -*-
import webapp2
import json


"""
Este Handler gerência as requisições
feitas a url /api/hello, nele é possível
definir por meio de funções qualquer 
verbo HTTP (GET, POST, PUT, DELETE...)
"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        """
        Método para gerênciar requisições GET.
        """
        message = {
            'msg': 'Hello Horld!'
        }

        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.write(json.dumps(message))


"""
O código abaixo utiliza o módulo WSGIApplication
para definir os endpoints da api rest,
ele recebe como parâmetro uma lista de tuplas,
onde cada tupla contém uma url e a referência
para o Handler que irá gerenciar todas as
requisições feitas a url que ele é responsável.
"""
app = webapp2.WSGIApplication([
    ('/api/hello', MainHandler)
], debug=True)