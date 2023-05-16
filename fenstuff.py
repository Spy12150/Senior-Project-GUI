class fenstuff:
    def __init__():
            pass
    def boardtofen(self,fen):
        
        binary = ''
        for element in fen:
            if(element == "P"):
                binary += "0100000"
            elif(element == "R"):
                binary += "0010000"
            elif(element == "N"):
                binary += "0001000"
            elif(element == "B"):
                binary += "0000100"
            elif(element == "Q"):
                binary += "0000010"
            elif(element == "K"):
                binary += "0000001"
            elif(element == "p"):
                binary += "1100000"
            elif(element == "r"):
                binary += "1010000"
            elif(element == "n"):
                binary += "1001000"
            elif(element == "b"):
                binary += "1000100"
            elif(element == "q"):
                binary += "1000010"
            elif(element == "k"):
                binary += "1000001"
            elif(element == "1"):
                binary += "0000000"
            elif(element == "2"):
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "3"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "4"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "5"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "6"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                
            elif(element == "7"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "8"):
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
                binary += "0000000"
            elif(element == "w"):
                binary += "0"
            elif(element == "b"):
                binary += "1"


        

    