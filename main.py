from Searcho import Searcho

from tools.SelectMenu import SelectMenu
from tools.TimeCounter import TimeCounter



def main():
    print("""
    Hugo Martinet
    Option OSY 2018-2019
    
    PROJET FRI-WEB

    Deux collections sont disponibles : CACM et CS276
    """)

    choose_collection(Searcho())

def choose_collection(engine):

    # Choix de la collection à traiter
    menu_collection = SelectMenu('Quelle collection choisissez-vous ?', ['CACM', 'CS276'])
    choice_collection = menu_collection.run()

    choose_action(choice_collection, engine)


def choose_action(choice_collection, engine):

    # Choix de l'action à effectuer sur la collection choisie
    if choice_collection == 0:
        menu_action = SelectMenu('Que voulez-vous faire ?', ['Lancer le moteur de recherche', 'Analyser la pertinence', 'Questions du TD', 'Retour'])
        choice_action = menu_action.run()
    elif choice_collection == 1:
        menu_action = SelectMenu('Que voulez-vous faire ?', ['Lancer le moteur de recherche (Booléen seulement)', 'Questions du TD', 'Retour'])
        choice_action = menu_action.run()

    if (choice_collection == 0 and choice_action == 3) or (choice_collection == 1 and choice_action == 2):
        choose_collection(engine)

    load_collection(choice_collection, engine)

    if choice_action == 0:
        launch_search_engine(choice_collection, engine)
    elif (choice_collection == 0 and choice_action == 2) or (choice_collection == 1 and choice_action == 1):
        answer_td_questions(choice_collection, engine)
    elif choice_collection == 0 and choice_action == 1:
        analyse_pertinence(choice_collection, engine)


def load_collection(choice_collection, engine):
    chrono = TimeCounter()

    # ON TESTE SI LA COLLECTION N'EST PAS DÉJÀ CHARGÉE
    coll = engine.active_collection
    if coll == '' or (coll == 'Cacm' and choice_collection == 1) or (coll == 'Cs276' and choice_collection == 0):
        # On lit les documents de la collection choisie
        print('Reading documents...')
        chrono.start()
        if choice_collection == 0:
            engine.read_cacm_collection()
        else:
            engine.read_cs276_collection()
        chrono.stop_and_print()

        # On crée l'index à partir des documents lus
        print('Creating index...')
        chrono.start()
        if choice_collection == 0:
            engine.create_index_cacm()
        elif choice_collection == 1:
            engine.create_index_cs276()
        chrono.stop_and_print()

    
def launch_search_engine(choice_collection, engine):
    chrono = TimeCounter()

    # CHOIX DU MODELE DE RECHERCHE
    choice_model = 0
    if choice_collection == 0:
        menu_model = SelectMenu('Quel modèle de recherche ?', ['Booléen', 'Vectoriel'])
        choice_model = menu_model.run()
    
    # SI MODELE BOOLEEN
    if choice_model == 0:
        print('<Type "quit searcho" to leave>')
        instruction = input('Search (use AND, OR or NOT) : ')
        while instruction != 'quit searcho':
            chrono.start()

            # on print les refs des documents retournés
            results = engine.boolean_request(instruction.lower().split(' '))
            if len(results) == 0:
                print('No results...')
            for doc_id in results:
                print(engine.docs[doc_id].ref)

            chrono.stop_and_print()
            instruction = input('Search (use AND, OR or NOT) : ')


    # SI MODELE VECTORIEL (SEULEMENT POUR CACM)
    elif choice_model == 1:
        print('Vectorizing...')
        chrono.start()
        engine.vectorize()
        chrono.stop_and_print()

        print('<Type "quit searcho" to leave>')

        instruction = input('Search (vectorial) : ')
        while instruction != 'quit searcho':
            chrono.start()
            print(engine.vectorial_request(instruction.split(' ')))
            chrono.stop_and_print()
            instruction = input('Search (vectorial) : ')

    # Retour au menu précédent
    print('\n\n')
    choose_action(choice_collection, engine)


def answer_td_questions(choice_collection, engine):
    question_choice = 0

    # Choix de la question du TD à répondre
    while question_choice != 5:
        questions_menu = SelectMenu("Choisissez une question de l'énoncé : ",
            ["1. Combien y a-t-il de tokens dans la collection ?",
            "2. Quelle est la taille du vocabulaire ?",
            "3. Déterminer les paramètres k et b de la loi de Heap.",
            "4. Estimer la taille du vocabulaire pour une collection de 1 million de tokens.",
            "5. Tracer le graphe fréquence (f) vs rang (r), puis log(f) vs log(r) ",
            "Retour"])
        question_choice = questions_menu.run()
        if question_choice == 0:
            engine.question1()
        elif question_choice == 1:
            engine.question2()
        elif question_choice == 2:
            engine.question3()
        elif question_choice == 3:
            engine.question4()
        elif question_choice == 4:
            engine.question5()
    

    print('\n\n')
    choose_action(choice_collection, engine)


def analyse_pertinence(choice_collection, engine):
    pass


if __name__ == '__main__':
    main()
