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
                --changename <old_name> <new_name>
                
                --listsites
                --setsite <site_name>
                
                --history
                            -fn/--filtername <name>
                            --add <name> <se> <ep>

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
changename_msg = 'Muda o nome do anime na base de dados.'

update_msg = 'Atualiza os animes e eps da base de dados.'
listsites = 'Lista os sites disponíveis.'
setsite = 'Seleciona um site.'

history_msg = 'Mostra o histórico de uso do -w e -wl.'
fn_msg = 'Filtra pelo nome passado.'
add_msg = 'Adiciona ou atualiza no histórico.'