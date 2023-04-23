# AniManage

AniManage é um Command Line Interface (CLI), onde você pode gerenciar e acessar sites de animes através do terminal. Com ele você pode listar os últimos episódios e animes lançados, pegar informações de um anime especifico e redirecionar para um episódio especifico ou para o mais recente através de um único comando.

## Instalação
1. Antes de tudo é preciso ter o python instalado. Você pode instala-lo [aqui](https://www.python.org/downloads/).

2. Clone este repositório:
   - ```git clone https://github.com/LeandroDeJesus-S/animanage.git```

3. Vá até o diretório:
   - ```cd animanage```

4. Faça o download das dependências usando o seguinte comando:
   - ```pip install -r requirements.txt```

 Se tudo estiver certo você já está pronto para usar :)
 
 ---
 
## Utilização
Obs: se você estiver utilizando linux e o comando ```python``` não seja reconhecido, tente substitui-lo por ```python3```.


Listando lançamentos de animes:
```python
python ani.py -la
```
![la cmd](https://user-images.githubusercontent.com/114845576/233846392-2a39162b-6f19-4be6-8873-0f31fd7cf1e8.png)

Listando os lançamentos de episódios:
```python
python ani.py -le
```
![le cmd](https://user-images.githubusercontent.com/114845576/233846644-e95afcdd-aa18-49ff-a744-c40a67808e10.png)<br>
Observe que os eps em cor verde são episódios novos (azul para animes), que ainda não foram salvos na base de dados.

Atualizar listagem de animes e episódios em lançamento:
```python
python ani.py --update
```
![update cmd](https://user-images.githubusercontent.com/114845576/233849821-adb56d30-0037-4a69-8df4-1d307629eb63.png)<br>
Obs: O update é feito automaticamente quando o programa é executado após 3 dias.

Buscando um anime:
```python
python ani.py --search "naruto"
```
![search cmd](https://user-images.githubusercontent.com/114845576/233847279-002a074d-1d29-4c59-b74d-ad6839edc74f.png)

Ir ao episódio mais recente de um anime:
```python
python ani.py -wl "Naruto"
```

Ir para um episódio especifico:
```python
python ani.py -w "Naruto" -s 1 -e 45
# ou também
python ani.py --watch "Naruto" --season 1 --ep 45
```
Obs: Caso não sejam especificados -s e -e o padrão para ambos é 1.

Ver informações de um anime:
```python
python ani.py --getinfo "Devilman: Crybaby"
```
![getinfo cmd](https://user-images.githubusercontent.com/114845576/233848071-17c4add4-9532-47a3-b2f4-07c1cb726647.png)

Listar os episódios do anime:
```python
python ani.py --listeps "Boku no Hero Academia"
```
![listeps cmd](https://user-images.githubusercontent.com/114845576/233848257-393b496d-7f8f-4aea-a820-08621f239c8e.png)

Mudar o nome de um anime:
```
# De "Boku no Hero Academia" para "Boku no hero"
python ani.py --changename "Boku no Hero Academia" "Boku no hero"
```
![changename cmd](https://user-images.githubusercontent.com/114845576/233848811-e133ad2b-6630-4637-83c5-2c4aa65507ec.png)

Ver os sites disponíveis:
```python
python ani.py --listsites
```
![listsites cmd](https://user-images.githubusercontent.com/114845576/233848963-5f8afc6a-5580-40b2-974a-395d65e082ab.png)<br>
Observe que o site com o "*" é site que está sendo utilizado. Para mudar de site você pode usar o seguinte comando:
```python
python ani.py --changesite "nome do site"
```

Ver historico:
```python
python ani.py --history
```
![history cmd](https://user-images.githubusercontent.com/114845576/233850211-5a81f1ef-046b-4f5d-8d02-dd6f7c12a5c3.png)<br>
Obs: O histórico faz o registro a partir dos comandos -w e -wl

Você também pode filtra por um anime em especifico usando a flag -fn ou --filtername:
```python
python ani.py --history -fn "naruto"
```
![history fn cmd](https://user-images.githubusercontent.com/114845576/233850396-e54290d9-b5ab-4aa6-8b51-2ad4e7bacf41.png)

Para adicionar use a flag --add passando o nome, numero da temporada e do episódio:
```python
python ani.py --history --add "naruto" 1 45
```
Obs: caso o anime já exista no histórico ele será atualizado com o número da temporada e do episódio.

Para remover do histórico use a flag -r ou --remove:
```python
python ani.py --history -r "naruto"
```
![history r remove cmd](https://user-images.githubusercontent.com/114845576/233851105-eb71a942-4620-4654-b811-ac1444bbec0d.png)


## Contribuindo

Contribuições são bem-vindas! Para fazer uma contribuição, siga as instruções abaixo:

1. Fork este repositório
2. Crie uma nova branch com o nome da sua feature (`git checkout -b minha_feature`)
3. Faça as alterações necessárias
4. Commit suas alterações (`git commit -m 'Adiciona minha_feature'`)
5. Push para a branch (`git push origin minha_feature`)
6. Abra um Pull Request

## Licença
Este projeto está sob a Licença [MIT](https://choosealicense.com/licenses/mit/)

AVISO: O programa foi desenvolvido e disponibilizado para uso próprio. Não me responsabilizo por uso improprio ou indevido do programa, nem tenho intensão de ferir ou prejudicar os direitos autorais dos sites utilizados. Caso proprietário de algum dos sites não estejam de acordo com o uso basta entrar em contado para que o problema seja resolvido.

Sites utilizados:
- [Animes Online](https://animesonlinecc.to/)
- [AnimesBr](https://animesbr.cc/)
- [Animes Online.online](https://ww31.animesonline.online/)

### Autor
---

<a href="">
 <img style="border-radius: 50%;" src="https://user-images.githubusercontent.com/114845576/233851586-92105a56-90ac-449b-ad5d-09c78ab8a511.jpg" width="100px;" alt=""/>
 <br />
 <sub><b>Leandro de Jesus Santos</b></sub></a> <a href="https://www.instagram.com/_leandro_zz/">🚀</a>


Feito por Leandro de Jesus Santos 
# Contato:

Email: [leandrojs@proton.me](mailto:leandrojs@proton.me) • 
instagram: [@_leandro_zz](https://www.instagram.com/_leandro_zz/)


