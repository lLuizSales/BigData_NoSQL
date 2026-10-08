#!/bin/bash

# Lê cada linha do arquivo CSV
while IFS=, read -r chave valor; do
    # Envia a chave e o valor para o Redis usando curl
    curl "http://localhost:5000/set/$chave/$valor"
    echo " Inserido $chave: $valor"
done < dados.csv
