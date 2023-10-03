import sqlite3

conexao = sqlite3.connect('agenda.db')
cursor = conexao.cursor()

cursor.execute("""
                create table patrimonio(
                id integer primary key,
                tombo varchar(100),
                local varchar(100)
                )""")
cursor.execute("insert into patrimonio (tombo, local) values (?,?)", ('355090','lab1'))
conexao.commit()
cursor.close()
conexao.close()
