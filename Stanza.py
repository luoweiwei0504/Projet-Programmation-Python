from installBackground import installBackground
import io

class MethodeDeStanza: 
    def tokenize_par_stanza(xml_file,xpath_expression):
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
                import stanza
            except ImportError:
                installBackground.install_Stanza()
                try:
                    import stanza
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            tree = etree.parse(xml_file)
            text_elements = tree.xpath(xpath_expression)
            text_total=''
            for element in text_elements:
                text_total+= element.text
            # charger les modèles françaises de tokeniser
            stanza.download('fr')
            nlp = stanza.Pipeline('fr', processors='tokenize')
            # tokeniser 
            doc = nlp(text_total)
            
            index=1
            conllu_output = ""
            #faire deux boucles pour convertir les tokens en conllu str
            for sentence  in doc.sentences:
                for token in sentence.tokens:
                    conllu_output += f"{index}\t{token.text}\t_\t_\t_\t_\t_\t_\t_\t|Offset={token.start_char}\n"
                    index+=1
            return conllu_output
        except Exception as e:
            return "Erreur :"+e

    
    def UPOS_par_Stanza(conllu_input):
        try:
            try:
                import stanza
                from stanza.utils.conll import CoNLL
                from stanza.models.common.doc import Document
            except ImportError:
                installBackground.install_Stanza()
                try:
                    import stanza
                    from stanza.utils.conll import CoNLL
                    from stanza.models.common.doc import Document
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            stanza.download('fr')
            nlp = stanza.Pipeline('fr', processors='tokenize,mwt,pos', tokenize_pretokenized=True)

            data_file=io.StringIO(conllu_input)
            # charger les chaînes de caractères en format CoNLL-u 
            doc, _ = CoNLL.load_conll(data_file)
            # convertir le format CoNLL-u en dictionnaire
            doc_dict = CoNLL.convert_conll(doc)
            r1=Document(doc_dict)
            # POS
            res=nlp(r1)
            res_dic=res.to_dict()
            # reconvertir le format dictionnaire en CoNLL-u
            doc_conll = CoNLL.convert_dict(res_dic)
            # sortir le format CoNLL-u par str
            conll_str = CoNLL.conll_as_string(doc_conll)
            return conll_str
        except Exception as e:
            return "Erreur :"+e


    def Lem_Par_Stanza(conllu_input):
        try:
            try:
                import stanza
                from stanza.utils.conll import CoNLL
                from stanza.models.common.doc import Document
            except ImportError:
                installBackground.install_Stanza()
                try:
                    import stanza
                    from stanza.utils.conll import CoNLL
                    from stanza.models.common.doc import Document
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            stanza.download('fr')
            nlp = stanza.Pipeline('fr', processors='tokenize,lemma', lemma_pretagged=True,          tokenize_pretokenized=True)

            data_file=io.StringIO(conllu_input)
            doc, _ = CoNLL.load_conll(data_file)
            doc_dict = CoNLL.convert_conll(doc)
            r1=Document(doc_dict)
            # remplir la colonne de Lemme
            res=nlp(r1)
            res_dic=res.to_dict()
            doc_conll = CoNLL.convert_dict(res_dic)
            conll_str = CoNLL.conll_as_string(doc_conll)
            return conll_str
        except Exception as e:
            return "Erreur :"+e
    
    #pour utiliser cette  méthodes, il faut avoir les labels de POS en avance.
    def dependency_parsing_par_Stanza(conllu_input):
        try:
            try:
                import stanza
                from stanza.utils.conll import CoNLL
                from stanza.models.common.doc import Document
            except ImportError:
                installBackground.install_Stanza()
                try:
                    import stanza
                    from stanza.utils.conll import CoNLL
                    from stanza.models.common.doc import Document
                except ImportError:
                    print ("Erreur,L'importation de modules/objets a échoué")

            stanza.download('fr')
            nlp = stanza.Pipeline('fr', processors='depparse',depparse_pretagged=True)

            data_file=io.StringIO(conllu_input)
            # Conll-U str -> Conll-U format
            doc, _ = CoNLL.load_conll(data_file)
            # Conll-U format -> dict
            doc_dict = CoNLL.convert_conll(doc)
            r1=Document(doc_dict)
            # remplir la Lemme
            res=nlp(r1)
            res_dic=res.to_dict()
            #  dict -> Conll-U format
            doc_conll = CoNLL.convert_dict(res_dic)
            # Conll-U format -> str
            conll_str = CoNLL.conll_as_string(doc_conll)
            return conll_str
        except Exception as e:
            return "Erreur :"+e
