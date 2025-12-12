#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Echo - Exemplo de Socket TCP
Devolve qualquer mensagem que recebe (echo).
Pode processar múltiplas conexões sequencialmente.
"""

import socket
import threading

def atender_cliente(conexao, endereco):
    print(f'Atendendo cliente {endereco}')

    try:
        while True:
            dados = conexao.recv(1024)

            if not dados:
                print(f'Cliente {endereco} desconectou')
                break

            mensagem = dados.decode('utf-8')
            print(f'Recebido de {endereco}: {mensagem}')

            resposta = f'Echo: {mensagem}'
            conexao.send(resposta.encode('utf-8'))

    except Exception as e:
        print(f'Erro com cliente {endereco}: {e}')

    finally:
        conexao.close()
        print(f'Conexão encerrada com {endereco}')



servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 5000))
servidor.listen(5)
print('Servidor Echo escutando em localhost:5000')

while True:
    print('\nAguardando conexão...')
    conexao, endereco = servidor.accept()
    print(f'Conectado com {endereco}')

    t = threading.Thread(target=atender_cliente, args=(conexao, endereco))
    t.daemon = True
    t.start()