import os
import sys
import requests
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        try:
            # Tenta ler o CSV
            cache = pd.read_csv('cache.csv')
            userEmCache = False

            # Verifica se o usuário já está em cache e imprime na tela se sim
            for nome in cache.username:
                if username == nome:
                    print(cache.loc[cache['username'] == username, ['email','website','hemisferio']].to_string(index=False))
                    userEmCache = True
                    break
            
            if userEmCache == False:
                # Pega os dados da API se o usuário não está em cache
                request = requests.get('https://jsonplaceholder.typicode.com/users')
                users = pd.DataFrame(request.json())
                user = users.loc[users['username'] == username, ['email','website']]

                # Descobre se hemisfério é Norte ou Sul
                for address in users.loc[users['username'] == username, 'address']:
                    if float(address['geo']['lat']) > 0:
                        hemisphere = 'Norte'
                    else:
                        hemisphere = 'Sul'
                        
                # Salva o usuário em cache e imprime na tela        
                additional_data = pd.DataFrame({'hemisferio': hemisphere, 'username': username}, index = user.index)
                user = user.join(additional_data)
                cache = cache.append(user)
                cache.to_csv('cache.csv', index=False)
                print(user[['email','website','hemisferio']].to_string(index=False))
                    
        # Se não conseguir ler o CSV, é porque está vazio                 
        except:
            # Pega os dados da API
            request = requests.get('https://jsonplaceholder.typicode.com/users')
            users = pd.DataFrame(request.json())
            user = users.loc[users['username'] == username, ['email','website']]
            
            # Descobre se hemisfério é Norte ou Sul
            for address in users.loc[users['username'] == username, 'address']:
                if float(address['geo']['lat']) > 0:
                    hemisphere = 'Norte'
                else:
                    hemisphere = 'Sul'
            
            # Salva o usuário em cache e imprime na tela
            additional_data = pd.DataFrame({'hemisferio': hemisphere, 'username': username}, index = user.index)
            user = user.join(additional_data)
            user.to_csv('cache.csv', index=False)
            print(user[['email','website','hemisferio']].to_string(index=False))

    else:
        print("Por favor, passe um username. Por exemplo: python main.py username")