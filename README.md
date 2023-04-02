# Génération de messages aléatoires (chaine de Markov)
À partir d'une conversation extraite dans un .txt dans mon cas (avec accord des intéressés), le code devrait être adaptable.  
`main.py` créé le dictionnaire pour la génération des messages à partir du txt et le sauvegarde dans un fichier ou le charge s'il existe déjà. Chaque mot est associé à un id pour que le fichier ne soit pas trop gros, du coup il y a table des ids + dict.  
`parser.py` c'est juste pour filtrer les messages suivant le template du .txt que j'avais.  
On peut spécifier l'auteur du message pour piocher seulement dans les mots qu'il a lui-même utilisé.
