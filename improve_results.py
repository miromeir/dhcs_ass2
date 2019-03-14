import pywikibot
from pywikibot import pagegenerators as pg
import codecs
import sys

def isLocation(name):
    with open('my_query.rq', 'r') as query_file:
        
        # load query from file, plant name inside query search
        QUERY = query_file.read().replace("######",name)

        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

        item = None
        try: 
            item = next(generator)
        except Exception as e:
            pass

        if item:
            return True

        else:
            return False

def isPerson(name):
    with open('person_query.rq', 'r') as query_file:
        
        # load query from file, plant name inside query search
        QUERY = query_file.read().replace("######",name)

        wikidata_site = pywikibot.Site("wikidata", "wikidata")
        generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

        item = None
        try: 
            
            for item in generator:
                item.get()
                he_label = item.labels.get("he")
                print("("+name+","+he_label+")")
                if (" "+name in he_label) or (name+" " in he_label):
                    return True

            return False
        except Exception as e:
            return False


def modifyLine(fileName, lineIndex, newValue):
    with codecs.open(fileName,'r+',encoding='utf-8',errors='ignore') as myFile:
        myFile.seek(0)
        
        pos = 0
        i=0
        while True:
            if i == lineIndex:
                try:
                    myFile.seek(pos)
                    myFile.write(newValue)
                    myFile.flush()
                    break
                except Exception as e:
                    print(e)
            else:
                x = len(myFile.readline().encode('utf-8'))
                
                pos = pos + x
            
            i = i+1
            
        

def main():
    INPUT_FILE = sys.argv[1]

    with open(INPUT_FILE, 'r',encoding='utf-8',errors='ignore') as myFile:
        lines = myFile.readlines()

        line_index = 0
        for line in lines:
            print("line#"+str(line_index))
            tagger_columns = line.strip().split(" ")
                
                # Don't use lines with less than 12 entries
            if len(tagger_columns) >= 12:
                    word = line.strip().split(" ")[3]
                    
                    # Don't check words that are punctuations , to save time
                    if len(word) > 1:
                        entity_type = ""
                        
                        for entity in ["I_LOC","B_LOC","I_PERS","I_ORG","I_DATE"]:
                            if entity in line.strip().split(" ")[11]:
                                entity_type = entity
                                break
                        
                        is_location = isLocation(word)
                        
                        # If this word doesnt have particular entity, still recognized as location, add I_LOC to it
                        if entity_type not in ["I_LOC","B_LOC","I_PERS","I_ORG","I_DATE"] and is_location:
                            
                            tagger_columns[11] = "I_LOC null"
                            tagger_columns[9] = (tagger_columns[9])[0:-3]
                        
                            new_value = " ".join(tagger_columns)
                            
                            try:
                                modifyLine(INPUT_FILE, line_index, new_value +"\n")
                                print(word+"="+"I_LOC")
                                print("exception")
                            except Exception as e:
                                pass
                        
                        #restore tagger_columns
                        tagger_columns = line.strip().split(" ")

                        is_person = isPerson(word)
                        if entity_type not in ["I_LOC","B_LOC","I_PERS","I_ORG","I_DATE"] and is_person:
                            
                            tagger_columns[11] = "I_PERS null"
                            tagger_columns[9] = (tagger_columns[9])[0:-4]
                        
                            new_value = " ".join(tagger_columns)
                            try:
                                modifyLine(INPUT_FILE, line_index, new_value +"\n")
                                print(word+"="+"I_PERS")
                            except Exception as e:
                                print("exception")
                                pass

            
            
            line_index = line_index + 1
        
if __name__ == "__main__":
    main()