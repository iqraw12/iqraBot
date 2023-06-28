from pyswip import Prolog

prolog = Prolog()
prolog.consult("D:/Chat_Bot/kb.pl")
print(list(prolog.query("male('Ali').")))




# def write_fact_and_rules(query):
#     with open('knowledge_Base.pl', 'a') as kb_file:
#         kb_file.write(query + '.\n')

# write_fact_and_rules("male('Ali')")
# def get_results(query):
#     results = list(prolog.query(query))
#     print(results)