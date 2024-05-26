from installBackground import installBackground
class XmlToConll_U:
    #méthode de tokeniser et traiter le fichier xml
    def tokenize_xml(xml_file, xpath_expression):
        try:
            # importe les outils
            try:
                from lxml import etree
            except ImportError:
                installBackground.install_lxml()
                try:
                    from lxml import etree
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            try:
                import nltk
            except ImportError:
                installBackground.install_NLTK()
                try:
                    import nltk
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

                
            nltk.download('punkt')
            tree = etree.parse(xml_file)
            #'identifier les zones de texte à traiter
            text_elements = tree.xpath(xpath_expression)
            text_total=''
            for element in text_elements:
                text_total+= element.text
            tokens = []
            offset = 0
            start_offset = 0
            for element in text_elements:
                text = element.text
                tokenized_text = nltk.word_tokenize(text)
                # ! il n'arrive pas à identifier <>
                for token in tokenized_text:
                    offset_La_fin_du_mot_dans_test = text_total[offset:].find(token)+len(token)
                    if text_total[offset_La_fin_du_mot_dans_test+offset]==" ":
                        space_after="Yes"
                        start_offset += offset
                        offset=len(token)+1
                    else:
                        space_after="No"
                        start_offset += offset
                        offset=len(token)

                    # ajouter les tokens et ses informations à la liste de tokens
                    tokens.append((token, start_offset, space_after))
            
            # génériser la sortie de CoNLL-U
            conllu_output = ""
            for idx, token in enumerate(tokens, start=1):
                token_str, start_offset, space_after = token
                #il faut utiliser la version python3.6 ou supérieur pour l'utilisateur comme ici on utilise la  farmat f=string
                conllu_output += f"{idx}\t{token_str}\t_\t_\t_\t_\t_\t_\t_\tSpaceAfter={space_after}|Offset={start_offset}\n"
            return conllu_output
        except Exception as e:
            return "Erreur :"+str(e)
        
        
