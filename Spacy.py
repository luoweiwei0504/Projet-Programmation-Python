from installBackground import installBackground
import io

# pour utiliser les méthodes, il faut avoir des données de la  première et la deuxième colonne   
class MethodeDeSpacy:
    @staticmethod
    def conllu_to_spacy(text):
        sentences = text.strip().split('\n\n')
        spacy_sentences = []
        for sentence in sentences:
            spacy_sentences.append([line.split('\t') for line in sentence.split('\n')])
        return spacy_sentences

    @staticmethod
    def spacy_to_conllu(spacy_sentences):
        conllu_text = ""
        for token in spacy_sentences:
            conllu_text += '\t'.join(token) + '\n'
        conllu_text += '\n'
        return conllu_text.strip()
    
    #méthode pour tokeniser 
    def tokenize_par_Spacy(xml_file,xpath_expression):
        #importe les outils 
        try:
            try:
                from lxml import etree
            except ImportError:
                installBackground.install_lxml()
                try:
                    from lxml import etree
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            try:
                import spacy
                from spacy.cli import download as spacy_download
                from spacy.tokens import Doc
            except ImportError:
                installBackground.install_spacy()
                try:
                    import spacy
                    from spacy.cli import download as spacy_download
                    from spacy.tokens import Doc
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            # charger les modèles de la langue française
            model_name = "fr_core_news_sm"
            if not spacy.util.is_package(model_name):
                spacy_download(model_name)
            nlp = spacy.load(model_name)

            tree = etree.parse(xml_file)
            text_elements = tree.xpath(xpath_expression)
            text_total=''
            for element in text_elements:
                text_total+= element.text
            
            # utiliser spacy pour traiter le texte
            doc = nlp(text_total)

            # tokeniser
            tokens = [token.text for token in doc if token.text.strip()]

            conllu_output=""
            index=1
            for token in tokens:
                conllu_output += f"{index}\t{token}\t_\t_\t_\t_\t_\t_\t_\t_\n"
                index+=1
            return conllu_output
        except Exception as e:
            return "Erreur :"+e




   
    #remplir la troisième colonne de conll_U en utilisant spacy(Lemmatization)
    def Lemme_par_Spacy(conllu_input:str):
        #importe les outils 
        try:
            try:
                import spacy
                from spacy.cli import download as spacy_download
                from spacy.tokens import Doc
            except ImportError:
                installBackground.install_spacy()
                try:
                    import spacy
                    from spacy.cli import download as spacy_download
                    from spacy.tokens import Doc
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            # charger les modèles de la langue française
            model_name = "fr_core_news_sm"
            if not spacy.util.is_package(model_name):
                spacy_download(model_name)
            nlp = spacy.load(model_name)
            # nlp = spacy.load('fr_core_news_sm')  
            spacy_sentences = MethodeDeSpacy.conllu_to_spacy(conllu_input)[0]

            words = [token[1] for token in spacy_sentences]

            def custom_tokenizer(nlp):
                # définir les règles de tokeniser
                def tokenize(text):
                    words = text.split(' ')  # l'utilisateur peut utiliser ses règles ici
                    return words

                # tokeniseur
                def tokenizer(text):
                    words = tokenize(text)
                    spaces = [True] * len(words)
                    return Doc(nlp.vocab, words=words, spaces=spaces)

                return tokenizer

            nlp.tokenizer = custom_tokenizer(nlp) 
            spacy_doc = nlp(' '.join(words))
            #parcourt chaque token et les correspondent avec leur lemme
            for i, token in enumerate(spacy_doc):
                spacy_sentences[i][2] = token.lemma_
            return MethodeDeSpacy.spacy_to_conllu(spacy_sentences)
        except Exception as e:
            return "Erreur :"+e        
    

    #########################################
    #    remplir la quatrième colonne      #
    #           (POS tagging)              #
    ########################################
    def Pos_par_Spacy(conllu_text:str):
        try:
            try:
                import spacy
                from spacy.cli import download as spacy_download
                from spacy.tokens import Doc
            except ImportError:
                installBackground.install_spacy()
                try:
                    import spacy
                    from spacy.cli import download as spacy_download
                    from spacy.tokens import Doc
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            # charger les modèles de la langue française
            model_name = "fr_core_news_sm"
            if not spacy.util.is_package(model_name):
                spacy_download(model_name)
            nlp = spacy.load(model_name)
            # nlp = spacy.load('fr_core_news_sm')  
            spacy_sentences = MethodeDeSpacy.conllu_to_spacy(conllu_text)[0]

            words = [token[1] for token in spacy_sentences]

            def custom_tokenizer(nlp):
                def tokenize(text):
                    words = text.split(' ')  # l'utilisateur peut utiliser ses règles ici
                    return words

                # tokeniseur
                def tokenizer(text):
                    words = tokenize(text)
                    spaces = [True] * len(words)
                    return Doc(nlp.vocab, words=words, spaces=spaces)

                return tokenizer
           
            nlp.tokenizer = custom_tokenizer(nlp) 
            spacy_doc = nlp(' '.join(words))
            #parcourt chaque token et remplir la septième et la quatrième colonne des tokens
            for i, token in enumerate(spacy_doc):
                spacy_sentences[i][3] = token.pos_
            return MethodeDeSpacy.spacy_to_conllu(spacy_sentences)
        except Exception as e:
            return "Erreur :"+e        

    ##################################################
    # remplir la septième et la huitième colonne   #
    #            (Dependency parsing)             #
    #################################################

    def dependency_parsing_par_Spacy(conllu_text):
        #importe les outils
        try:
            try:
                import spacy
                from spacy.cli import download as spacy_download
                from spacy.tokens import Doc
            except ImportError:
                installBackground.install_spacy()
                try:
                    import spacy
                    from spacy.cli import download as spacy_download
                    from spacy.tokens import Doc
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")
            # charger les modèles de la langue française
            model_name = "fr_core_news_sm"
            if not spacy.util.is_package(model_name):
                spacy_download(model_name)
            nlp = spacy.load(model_name)
            spacy_sentences = MethodeDeSpacy.conllu_to_spacy(conllu_text)[0]

            words = [token[1] for token in spacy_sentences]

            def custom_tokenizer(nlp):
                # définir les régles de tokeniser
                def tokenize(text):
                    words = text.split(' ')  # l'utilisateur peut utiliser ses règles ici
                    return words

                # tokeniseur
                def tokenizer(text):
                    words = tokenize(text)
                    spaces = [True] * len(words)
                    return Doc(nlp.vocab, words=words, spaces=spaces)

                return tokenizer

            nlp.tokenizer = custom_tokenizer(nlp) 
            spacy_doc = nlp(' '.join(words))
            #parcourt chaque token et remplir la septième et la huitième colonne des tokens
            for i, token in enumerate(spacy_doc):
                spacy_sentences[i][6] = str(token.head.i + 1) if token.dep_ != 'ROOT' else '0'
                spacy_sentences[i][7] = token.dep_
            return MethodeDeSpacy.spacy_to_conllu(spacy_sentences)
        except Exception as e:
            return "Erreur :"+e        
