from XmlToConll_U import XmlToConll_U
from Spacy import MethodeDeSpacy
from UDPipe import MethodeDeUDPipe
from Stanza import MethodeDeStanza

import sys

class Main:
    # pour parcour tous les methode 
    def test(nomdeDossier,xpath_expression):
        original_stdout = sys.stdout
        i=0
        j=0
        l=0
        k=0
        xpath_expression='//'+xpath_expression
        with open("output.txt", "w", encoding="utf-8") as file:
            sys.stdout = file
            for i in range(4):
                try:
                    if i==0:
                        Conll_U_Data=XmlToConll_U.tokenize_xml(nomdeDossier,xpath_expression)
                    if i==1:
                        Conll_U_Data=MethodeDeSpacy.tokenize_par_Spacy(nomdeDossier,xpath_expression)
                    if i==2:
                        Conll_U_Data=MethodeDeUDPipe.tokenize(nomdeDossier,xpath_expression)
                    if i==3:
                        Conll_U_Data=MethodeDeStanza.tokenize_par_stanza(nomdeDossier,xpath_expression)
                except Exception as e:
                    print("Erreur de tokenize par token: "+str(i)+" lemme: "+str(k)+" pos:"+str(j)+" dependcy:"+str(l))
                    print(e)

                for k in range (3):
                    try:
                        if k==0:
                            Conll_U_Data=MethodeDeSpacy.Lemme_par_Spacy(Conll_U_Data)
                        if k==1:
                            Conll_U_Data=MethodeDeUDPipe.Lemme_Par_UDPipe(Conll_U_Data)
                        if k==2:
                            Conll_U_Data=MethodeDeStanza.Lem_Par_Stanza(Conll_U_Data)
                    except Exception as e:
                        print("Erreur de lemme par token: "+str(i)+" lemme: "+str(k)+" pos:"+str(j)+" dependcy:"+str(l))
                        print(e)
                    for j in range(3):
                        try:
                            if j==0:
                                Conll_U_Data=MethodeDeSpacy.Pos_par_Spacy(Conll_U_Data)
                            if j==1:
                                Conll_U_Data=MethodeDeUDPipe.UPOS_Par_UDPipe(Conll_U_Data)
                            if j==2:
                                Conll_U_Data=MethodeDeStanza.UPOS_par_Stanza(Conll_U_Data)
                        except Exception as e:
                            print("Erreur de Pos par token: "+str(i)+" lemme: "+str(k)+" pos:"+str(j)+" dependcy:"+str(l))
                            print(e)
                        for l in range(3):
                            try:
                                if l==0:
                                    Conll_U_Data=MethodeDeSpacy.dependency_parsing_par_Spacy(Conll_U_Data)
                                if l==1:
                                    Conll_U_Data=MethodeDeUDPipe.dependency_parsing_par_UDPipe(Conll_U_Data)
                                if l==2:
                                    Conll_U_Data=MethodeDeStanza.dependency_parsing_par_Stanza(Conll_U_Data)
                                print("Methode de token: "+str(i)+" , lemme: "+str(k)+" pos: "+str(j)+" dependcy: "+str(l))
                                print(Conll_U_Data)
                            except Exception as e:
                                print("Erreur de depency par token: "+str(i)+" lemme: "+str(k)+" pos:"+str(j)+" dependcy:"+str(l))
                                print(e)
        sys.stdout = original_stdout
        return ("Fini")

    def interface():
        import tkinter as tk
        from tkinter import messagebox


        def on_submit():
            choices = f"Data Type: {data_type_var.get()}\n" \
                    f"Path: {path_entry.get()}\n" \
                    f"Tokenize: {tokenize_var.get()}\n" \
                    f"Lemme: {lemme_var.get()}\n" \
                    f"Pos: {pos_var.get()}\n" \
                    f"Dependency Parsing: {dependency_var.get()}\n" \
                    f"L'analyse resussi, le resultat est dans 'resultat.txt'. "
            

            if (data_type_var.get()=="XML"):
                if tokenize_var.get()=="nlp":
                    Conll_U_Data=XmlToConll_U.tokenize_xml(path_entry.get(),xpath_entry.get())
                elif tokenize_var.get()=="spacy":
                    Conll_U_Data=MethodeDeSpacy.tokenize_par_Spacy(path_entry.get(),xpath_entry.get())
                elif  tokenize_var.get()=="stanza":
                    Conll_U_Data=MethodeDeStanza.tokenize_par_stanza(path_entry.get(),xpath_entry.get())
                elif tokenize_var.get()=="UDPipe":
                    Conll_U_Data=MethodeDeUDPipe.tokenize(path_entry.get(),xpath_entry.get())
            else:
                with open(path_entry.get(),"r",encoding="utf-8") as file:
                    Conll_U_Data=file.read()

            if Conll_U_Data[:6]=="Erreur":
                messagebox.showinfo("Erreur massage", Conll_U_Data)
                return
            #Lemme
            if lemme_var.get()=="spacy":
                Conll_U_Data=MethodeDeSpacy.Lemme_par_Spacy(Conll_U_Data)
            elif lemme_var.get()=="UDPipe":
                Conll_U_Data=MethodeDeUDPipe.Lemme_Par_UDPipe(Conll_U_Data)
            elif lemme_var.get()=="stanza":
                Conll_U_Data=MethodeDeStanza.Lem_Par_Stanza(Conll_U_Data)

            if Conll_U_Data[:6]=="Erreur":
                messagebox.showinfo("Erreur massage",Conll_U_Data)
                return
            #Pos
            if pos_var.get()=="spacy":
                Conll_U_Data=MethodeDeSpacy.Pos_par_Spacy(Conll_U_Data)
            elif pos_var.get()=="UDPipe":
                Conll_U_Data=MethodeDeUDPipe.UPOS_Par_UDPipe(Conll_U_Data)
            elif pos_var.get()=="stanza":
                Conll_U_Data=MethodeDeStanza.UPOS_par_Stanza(Conll_U_Data)

            if Conll_U_Data[:6]=="Erreur":
                messagebox.showinfo("Erreur massage",Conll_U_Data)
                return
            #Dependency
            if dependency_var.get()=="spacy":
                Conll_U_Data=MethodeDeSpacy.dependency_parsing_par_Spacy(Conll_U_Data)
            elif dependency_var.get()=="UDPipe":
                Conll_U_Data=MethodeDeUDPipe.dependency_parsing_par_UDPipe(Conll_U_Data)
            elif dependency_var.get()=="stanza":
                Conll_U_Data=MethodeDeStanza.dependency_parsing_par_Stanza(Conll_U_Data)

            if Conll_U_Data[:6]=="Erreur":
                messagebox.showinfo("Erreur massage",Conll_U_Data)
                return
            
            with open("resultat.txt", "w", encoding="utf-8") as file:
                file.write(Conll_U_Data)                       
            messagebox.showinfo("Choices", choices)

        def on_data_type_change():
            if data_type_var.get() == "XML":
                tokenize_var.set("nlp")
                tokenize_none_btn.config(state="disabled")
                for btn in [tokenize_nlp_btn, tokenize_spacy_btn, tokenize_stanza_btn, tokenize_udpipe_btn]:
                    btn.config(state="normal")
            else:
                tokenize_var.set("None")
                tokenize_none_btn.config(state="normal")
                for btn in [tokenize_nlp_btn, tokenize_spacy_btn, tokenize_stanza_btn, tokenize_udpipe_btn]:
                    btn.config(state="disabled")

        def on_test_click(self):
            self.test(path_entry.get(),xpath_entry.get())
            messagebox.showinfo("Test", "Test Fini! Le resultat est dans output.txt")
            
        root = tk.Tk()
        root.title("Projet Programmation Python")

        # Type de donnee
        data_type_label = tk.Label(root, text="Type de donnee")
        data_type_label.grid(row=0, column=0, sticky="w")

        data_type_var = tk.StringVar()
        data_type_var.set("XML")

        xml_btn = tk.Radiobutton(root, text="XML", variable=data_type_var, value="XML", command=on_data_type_change)
        xml_btn.grid(row=1, column=0, sticky="w")
        conll_btn = tk.Radiobutton(root, text="Conll", variable=data_type_var, value="Conll", command=on_data_type_change)
        conll_btn.grid(row=1, column=1, sticky="w")

        # Nom et chemaine de donnee
        path_label = tk.Label(root, text="Nom et chemaine de donnee")
        path_label.grid(row=2, column=0, sticky="w")

        path_entry = tk.Entry(root)
        path_entry.grid(row=3, column=0, columnspan=2, sticky="we")

        # xpath_expression
        xpath_label = tk.Label(root, text="Xpath expression(Pas necessaire pour Conll)")
        xpath_label.grid(row=2, column=2, sticky="w")

        xpath_entry = tk.Entry(root)
        xpath_entry.grid(row=3, column=2, columnspan=2, sticky="we")

        # Tokenize si Le donnee est XML
        tokenize_label = tk.Label(root, text="Tokenize si Le donnee est XML")
        tokenize_label.grid(row=4, column=0, sticky="w")

        tokenize_var = tk.StringVar()
        tokenize_var.set("nlp")

        tokenize_nlp_btn = tk.Radiobutton(root, text="nlp", variable=tokenize_var, value="nlp")
        tokenize_nlp_btn.grid(row=5, column=0, sticky="w")
        tokenize_spacy_btn = tk.Radiobutton(root, text="spacy", variable=tokenize_var, value="spacy")
        tokenize_spacy_btn.grid(row=5, column=1, sticky="w")
        tokenize_stanza_btn = tk.Radiobutton(root, text="stanza", variable=tokenize_var, value="stanza")
        tokenize_stanza_btn.grid(row=5, column=2, sticky="w")
        tokenize_udpipe_btn = tk.Radiobutton(root, text="UDPipe", variable=tokenize_var, value="UDPipe")
        tokenize_udpipe_btn.grid(row=5, column=3, sticky="w")
        tokenize_none_btn = tk.Radiobutton(root, text="None", variable=tokenize_var, value="None", state="disabled")
        tokenize_none_btn.grid(row=5, column=4, sticky="w")

        # Lemme
        lemme_label = tk.Label(root, text="Lemme")
        lemme_label.grid(row=6, column=0, sticky="w")

        lemme_var = tk.StringVar()
        lemme_var.set("None")

        lemme_spacy_btn = tk.Radiobutton(root, text="spacy", variable=lemme_var, value="spacy")
        lemme_spacy_btn.grid(row=7, column=0, sticky="w")
        lemme_stanza_btn = tk.Radiobutton(root, text="stanza", variable=lemme_var, value="stanza")
        lemme_stanza_btn.grid(row=7, column=1, sticky="w")
        lemme_udpipe_btn = tk.Radiobutton(root, text="UDPipe", variable=lemme_var, value="UDPipe")
        lemme_udpipe_btn.grid(row=7, column=2, sticky="w")
        lemme_none_btn = tk.Radiobutton(root, text="None", variable=lemme_var, value="None")
        lemme_none_btn.grid(row=7, column=3, sticky="w")

        #Pos
        pos_label = tk.Label(root, text="Pos")
        pos_label.grid(row=8, column=0, sticky="w")

        pos_var = tk.StringVar()
        pos_var.set("None")

        pos_spacy_btn = tk.Radiobutton(root, text="spacy", variable=pos_var, value="spacy")
        pos_spacy_btn.grid(row=9, column=0, sticky="w")
        pos_stanza_btn = tk.Radiobutton(root, text="stanza", variable=pos_var, value="stanza")
        pos_stanza_btn.grid(row=9, column=1, sticky="w")
        pos_udpipe_btn = tk.Radiobutton(root, text="UDPipe", variable=pos_var, value="UDPipe")
        pos_udpipe_btn.grid(row=9, column=2, sticky="w")
        pos_none_btn = tk.Radiobutton(root, text="None", variable=pos_var, value="None")
        pos_none_btn.grid(row=9, column=3, sticky="w")

        #Dependency parsing
        dependency_label = tk.Label(root, text="Dependency parsing")
        dependency_label.grid(row=10, column=0, sticky="w")

        dependency_var = tk.StringVar()
        dependency_var.set("None")

        dependency_spacy_btn = tk.Radiobutton(root, text="spacy", variable=dependency_var, value="spacy")
        dependency_spacy_btn.grid(row=11, column=0, sticky="w")
        dependency_stanza_btn = tk.Radiobutton(root, text="stanza", variable=dependency_var, value="stanza")
        dependency_stanza_btn.grid(row=11, column=1, sticky="w")
        dependency_udpipe_btn = tk.Radiobutton(root, text="UDPipe", variable=dependency_var, value="UDPipe")
        dependency_udpipe_btn.grid(row=11, column=2, sticky="w")
        dependency_none_btn = tk.Radiobutton(root, text="None", variable=dependency_var, value="None")
        dependency_none_btn.grid(row=11, column=3, sticky="w")

        #Submit button
        submit_btn = tk.Button(root, text="Submit", command=on_submit)
        submit_btn.grid(row=12, column=0, columnspan=2, sticky="we")

        #Test button
        test_btn = tk.Button(root, text="Test", command=on_test_click)
        test_btn.grid(row=12, column=2, columnspan=2, sticky="we")

        root.mainloop()


    if __name__ == "__main__":
        interface()