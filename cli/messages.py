import sys

filename = sys.argv[0]


USAGE = f"""
        {filename}  -w <name>
                            -s/--season <n> -e/--ep <n>
            
                -wl/--watchlatest <name>
                
                -le
                -la
                
                --search <name>
                --getinfo <name>
                --listeps <name>
                --alias <current_name> <alias>
                
                --listsites
                --changesite <site_name>
                
                --history/-H
                            -fn/--filtername <name>
                            --add <name> <se> <ep>
                            -r/--remove <name>
                
                --add-anime <name> <url>

"""




w_msg = 'Redireciona para o anime passado.'
s_msg = 'Especifica um temporada.'
e_msg = 'Especifica um episódio.'

wl_msg = 'Redireciona para o ep mais recente.'

le_msg = 'Lista os episódios em lançamento.'
la_msg = 'Lista os animes em lançamento.'

search_msg = 'Busca por um anime na base de dados.'
getinfo_msg = 'Mostra algumas informações do anime.'
listeps_msg = 'Lista os eps do anime.'
alias_msg = 'Da um "apelido" para um anime.'

update_msg = 'Atualiza os animes e eps da base de dados para o site atual.'
update_all_msg = 'Atualiza os animes e eps da base de dados para todos os sites.'
listsites_msg = 'Lista os sites disponíveis.'
changesite_msg = 'Seleciona um site.'

history_msg = 'Mostra o histórico de uso do -w e -wl.'
fn_msg = 'Filtra pelo nome passado.'
add_msg = 'Adiciona ou atualiza no histórico.'
remove_msg = "remove um registro do histórico."
add_anime_msg = 'Adiciona um anime na base de dados.'
