# virtaamat-heroku

Käyttää plotlyä ja dashiä.

Yksinkertainen web app, joka piirtää paikkakohtaisen kuvaajan virtaamat datasta.

Tämä repo on tehty heroku deploymenttiä varten.

Input data: Paikka, Aika, Arvo

Arvo voi olla null, jolloin kuvaajaa ei piirretä siltä ajalta.

Algoritimi täyttää puuttuvat päivät aikasarjaan, koska jokaiselle päivälle ei aina ole riviä.
