from installBackground import installBackground
import urllib.request
import io
from pip._internal import main

class MethodeDeUDPipe:
    def tokenize(xml_file,xpath_expression):
        try:
            # importe les outils
            try:
                import ufal.udpipe

            except ImportError:
                installBackground.install_UDPipe()
                try:
                    import ufal.udpipe

                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            # outil lxml pour lire les fichiers de xml       
            try:
                from lxml import etree
            except ImportError:
                installBackground.install_lxml()
                try:
                    from lxml import etree
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            # lire le fichier xml
            tree = etree.parse(xml_file)
            text_elements = tree.xpath(xpath_expression)
            # mettre les textes à text_total
            text_total=''
            for element in text_elements:
                text_total+= element.text

            # charger les modèles 
            url = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
            filename = './modele/french-ud-2.5-191206.udpipe'
            # télécharger le fichier
            urllib.request.urlretrieve(url, filename)

            # charger les modèles
            model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')
            # créer pipeline UDPipe pour traiter les textes comme tokeniser, POS et analyse dépendante
            pipeline = ufal.udpipe.Pipeline(model, 'tokenizer', '', '', '')

            # process input text
            processed = pipeline.process(text_total)

            # extraire le  texte tokenisé 
            tokenlist = []
            for sentence in processed.split('\n'):
                tokens = sentence.split('\t')
                if len(tokens) == 10:  # skip empty lines
                    tokenlist.append([tokens[0],tokens[1],tokens[9]])

            # générer la sortie de CoNLL-U
            conllu_output = ""
            idx=0
            for token in tokenlist:
                if(len(token)==3):
                    if '-'  not in token[0]:
                        idx+=1
                        conllu_output += f"{idx}\t{token[1]}\t_\t_\t_\t_\t_\t_\t_\t{token[2]}\n"
            return conllu_output
        except Exception as e:
            return "Erreur :"+e
        
    #UPOS：les caractéristiques générales des mots comme la catégorie
    #XPOS：les caractéristiques pour certaines langues spécifiques comme le ton du mandarin
    def UPOS_Par_UDPipe(conllu_input):
        try:
            # importe les outils
            try:
                import ufal.udpipe

            except ImportError:
                installBackground.install_UDPipe()
                try:
                    import ufal.udpipe

                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")


            # télécharger les modèles 
            url = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
            filename = './modele/french-ud-2.5-191206.udpipe'
            # télécharger le fichier
            urllib.request.urlretrieve(url, filename)
            # télécharger le modèle
            model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')
            # créer la pipeline
            pipeline = ufal.udpipe.Pipeline(model, 'conllu', ufal.udpipe.Pipeline.DEFAULT, ufal.udpipe.Pipeline.DEFAULT, 'conllu')
            # traiter le texte d'entrée
            processed = pipeline.process(conllu_input)


            # extraire les textes tokenisés
            UPOSlist = []
            # parcourir  chqaue phrase et les tokeniser, et ajouter les tokens à la liste de UPOSlist
            for sentence in processed.split('\n'):
                tokens = sentence.split('\t')
                if len(tokens) == 10:  # passer les lignes vides
                    UPOSlist.append([tokens[3],tokens[4]])


            data_file = io.StringIO(conllu_input)
                
            # mettre chaque mot à une liste
            data_lines = data_file.readlines()

            new_data_lines = []
            index=0
            for line in data_lines:
                fields = line.strip().split('\t')
                if len(fields) == 10:
                    new_line = f"{fields[0]}\t{fields[1]}\t{fields[2]}\t{UPOSlist[index][0]}\t{UPOSlist[index][1]}\t{fields[5]}\t{fields[6]}\t{fields[7]}\t{fields[8]}\t{fields[9]}\n"
                    new_data_lines.append(new_line)
                    index+=1
            output_conll = ''.join(new_data_lines)
            return output_conll
        except Exception as e:
            return "Erreur :"+e


    
    #méthode de traiter la colonne de LEMMA
    def Lemme_Par_UDPipe(conllu_input):
        try:
            try:
                import ufal.udpipe
                

            except ImportError:
                installBackground.install_UDPipe()
                try:
                    import ufal.udpipe

                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            
            # charger les modèles 
            model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')
            if not model:
                # télécharger le modèle
                url = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
                filename = './modele/french-ud-2.5-191206.udpipe'
                # télécharger le fichier
                urllib.request.urlretrieve(url, filename)
                # charger le modèle
                model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')

            # créer la piprline
            pipeline = ufal.udpipe.Pipeline(model, 'conllu', ufal.udpipe.Pipeline.DEFAULT, ufal.udpipe.Pipeline.DEFAULT, 'conllu')
            # traiter le texte d'entrée
            processed = pipeline.process(conllu_input)
            
            Lemmelist = []
            for sentence in processed.split('\n'):
                tokens = sentence.split('\t')
                if len(tokens) == 10:  # passer les lignes vides 
                    Lemmelist.append(tokens[2])
            # convertir les donées de str en format conllu en le fichier à lire
            data_file = io.StringIO(conllu_input)
                
            # lire les donées du fichiers et mettre chaque mot dans une liste
            data_lines = data_file.readlines()

            new_data_lines = []
            index=0
            for line in data_lines:
                fields = line.strip().split('\t')
                if len(fields) == 10:
                    new_line = f"{fields[0]}\t{fields[1]}\t{Lemmelist[index]}\t{fields[3]}\t{fields[4]}\t{fields[5]}\t{fields[6]}\t{fields[7]}\t{fields[8]}\t{fields[9]}\n"
                    new_data_lines.append(new_line)
                    index+=1
            output_conll = ''.join(new_data_lines)
            return output_conll
        except Exception as e:
            return "Erreur :"+e    

    # #FEATS：les caractéristiques morphologiques des mots
    # def Feats_Par_UDPipe(conllu_input):
    #     try:
    #         import ufal.udpipe
            

    #     except ImportError:
    #         installBackground.install_UDPipe()
    #         try:
    #             import ufal.udpipe

    #         except ImportError:
    #             print ("Erreur,L'importation de modules/objets a échoué")
        
    #     
    #     model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')
    #     if not model:
    #         
    #         # set the download URL and local file name
    #         url = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
    #         filename = './modele/french-ud-2.5-191206.udpipe'
    #         # download the file
    #         urllib.request.urlretrieve(url, filename)
    #         model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')

    #     # créer la pipeline
    #     pipeline = ufal.udpipe.Pipeline(model, 'conllu', ufal.udpipe.Pipeline.DEFAULT, ufal.udpipe.Pipeline.DEFAULT, 'conllu')
    #    
    #     processed = pipeline.process(conllu_input)
        
    #     Featslist = []
    #     for sentence in processed.split('\n'):
    #         tokens = sentence.split('\t')
    #         if len(tokens) == 10:  # skip empty lines
    #             Featslist.append(tokens[5])
    #     
    #     data_file = io.StringIO(conllu_input)
            
    #     
    #     data_lines = data_file.readlines()

    #     new_data_lines = []
    #     index=0
    #     for line in data_lines:
    #         fields = line.strip().split('\t')
    #         if len(fields) == 10:
    #             new_line = f"{fields[0]}\t{fields[1]}\t{fields[2]}\t{fields[3]}\t{fields[4]}\t{Featslist[index]}\t{fields[6]}\t{fields[7]}\t{fields[8]}\t{fields[9]}\n"
    #             new_data_lines.append(new_line)
    #             index+=1
    #     output_conll = ''.join(new_data_lines)
    #     return output_conll


#HEAD：L'identifiant du nœud parent du mot dans l'arbre syntaxique
#DEPREL：Le type de relation de dépendance entre le mot et son nœud parent.
    #méthode pour traiter les colonnes de HEAD et DEPREL
    def dependency_parsing_par_UDPipe(conllu_input):
        try:
                # importe les outils et les ressources 
            try:
                import ufal.udpipe
                

            except ImportError:
                installBackground.install_UDPipe()
                try:
                    import ufal.udpipe

                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            

            model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')
            if not model:
                # télécharger les modèles
                url = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
                filename = './modele/french-ud-2.5-191206.udpipe'
                # télécharger le fichier
                urllib.request.urlretrieve(url, filename)
                # charger le modèle
                model = ufal.udpipe.Model.load('./modele/french-ud-2.5-191206.udpipe')

            # créer la pipeline
            pipeline = ufal.udpipe.Pipeline(model, 'conllu', ufal.udpipe.Pipeline.DEFAULT, ufal.udpipe.Pipeline.DEFAULT, 'conllu')
            # traiter le texte d'entrée
            processed = pipeline.process(conllu_input)
            
            HeadetDeprellist = []
            #parcourir chaque phrase et les traiter en sortie de token
            for sentence in processed.split('\n'):
                tokens = sentence.split('\t')
                if len(tokens) == 10:  # passer les lignes vides
                    HeadetDeprellist.append([tokens[6],tokens[7]])
            # convertir les donées de str en format conllu en le fichier à lire
            data_file = io.StringIO(conllu_input)
                
            # lire les donées du fichier et mettre chaque mot dans une liste
            data_lines = data_file.readlines()

            new_data_lines = []
            index=0
            for line in data_lines:
                fields = line.strip().split('\t')
                if len(fields) == 10:
                    new_line = f"{fields[0]}\t{fields[1]}\t{fields[2]}\t{fields[3]}\t{fields[4]}\t{fields[5]}\t{HeadetDeprellist[index][0]}\t{HeadetDeprellist[index][1]}\t{fields[8]}\t{fields[9]}\n"
                    new_data_lines.append(new_line)
                    index+=1
            output_conll = ''.join(new_data_lines)
            return output_conll
        except Exception as e:
            return "Erreur :"+e
