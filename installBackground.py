from pip._internal import main
class installBackground:
    @staticmethod
    def install_lxml():
        main(["install","lxml"])

    @staticmethod
    def install_spacy():
        main(["install","spacy"])

    @staticmethod
    def install_UDPipe():
        main(["install","ufal.udpipe"])
    
    @staticmethod
    def install_Stanza():
        main(["install","stanza"])
    
    @staticmethod
    def install_NLTK():
        main(["install","nltk"])
