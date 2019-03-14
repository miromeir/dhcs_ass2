import os
import sys
import lxml.etree

def main():
    POS_FILE = sys.argv[1]
    TEI_FILE = sys.argv[2]
    
    # Extract named entities from TEI file

    output_list = []

    with open(TEI_FILE, "r") as myFile:
        doc = lxml.etree.parse(myFile)
        ns = {"default":"http://www.tei-c.org/ns/1.0"}
        body = doc.getroot().find(".//default:body", namespaces=ns)
        per_name_org = body.xpath(".//*[(self::default:placeName) or (self::default:persName)]",namespaces=ns)
        
        
        for item in per_name_org:
            if "persName" in item.tag: 
                #if has surname / forename:
                if len(item.xpath(".//*[(self::default:surname) or (self::default:forename)]", namespaces=ns)) == 2:
                    output_list.append((("persName"),item.xpath(".//default:surname",namespaces = ns)[0].text))
                    output_list.append((("persName"),item.xpath(".//default:forename", namespaces = ns)[0].text))
                else:
                    #if value is more than one words, add seperate entries
                    for token in item.text.strip().split(" "):
                        output_list.append(("persName",token))

            if "placeName" in item.tag:
                #if value is more than one words, add seperate entries
                for token in item.text.strip().split(" "):
                    output_list.append(("placeName",token))


    tei_ents = iter(output_list)

    tagger_to_tei = {"I_LOC":"placeName", "B_LOC":"placeName", "I_PERS":"persName"}

    false_positive = 0
    false_negative = 0
    accurate = 0
    with open(POS_FILE, "r",encoding = 'utf-8',errors='ignore') as myFile:
        lines = myFile.readlines()
        next_tei = next(tei_ents)
        
        for line in lines:
            if len(line)>1:
                tagger_columns = line.strip().split(" ")
                
                # Don't use lines with less than 12 entries
                if len(tagger_columns) >= 12:
                    word = line.strip().split(" ")[3]
                
                    entity_type = ""
                    
                    for entity in ["I_LOC","B_LOC","I_PERS"]:
                        if entity in line.strip().split(" ")[11]:
                            entity_type = entity
                            break
                    
                    
                    if next_tei[1] in word:
                        if entity_type != "":
                            if tagger_to_tei.get(entity_type) == next_tei[0]:
                                print(entity_type+","+word+","+"accurate")
                                accurate = accurate + 1
                            else:
                                print(entity_type+","+word+","+"false_negative. expected:"+next_tei[0])
                                false_negative = false_negative + 1
                        else:
                            print(entity_type+","+word+","+"false_negative, expected:"+next_tei[0])
                            false_negative = false_negative + 1
                        try:
                            next_tei = next(tei_ents)
                        except Exception as e:
                            next_tei = ("NONE","NONE")

                    else:
                        if entity_type != "":
                            print(entity_type+","+word+","+"false_positive")
                            false_positive = false_positive + 1

        print("*****************************************")
        print("*************** TOTAL *******************")
        print(" - Accurate:"+str(accurate))
        print(" - False Positive:"+str(false_positive))
        print(" - False Negative:"+str(false_negative))
    
                        
                            
                        
                        
                            

                    
                    
    
                
if __name__ == '__main__':
    main()
