import os
import sys
from pypdf import PdfReader
import datasets
import tabulate

human_dataset = datasets.load_dataset("allenai/peS2o", "v2", split="train")

from grammer_rules import punctuationRules
from grammer_rules import scentenceStarters
from grammer_rules import sentenceStructure
from grammer_rules import structuralDiscourse
from grammer_rules import wordChoice

def list_files_in_directory(directory_path):
    files_list = []
    for entry_name in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry_name)
        if os.path.isfile(full_path):
            files_list.append(full_path)
    return files_list

all_measures = [
    punctuationRules.rules,
    scentenceStarters.rules,
    sentenceStructure.rule,
    structuralDiscourse.rule,
    wordChoice.rules
]

all_measures = [item for sublist in all_measures for item in sublist]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide a directory path to ai generated pdf files and then human written papers.")
        quit()

    print("Processing AI generated files...")  
    ai_directory_path = sys.argv[1]
    ai_files = list_files_in_directory(ai_directory_path)

    ai_stats = []
    for ai_file in ai_files:
        file_stats = []
        reader = PdfReader(ai_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        for measure in all_measures:
            file_stats.append(measure(text))

        ai_stats.append(file_stats)

    ai_avg_stats = []

    num_files = len(ai_stats)
    ai_avg_stats = [sum(measure_scores) / num_files for measure_scores in zip(*ai_stats)]

    print("Processing human generated files...")  
    #human_directory_path = sys.argv[2]
    #human_files = list_files_in_directory(human_directory_path)

    human_files = []
    for row in human_dataset:
        created = row.get("created")
        if created:
            try:
                # Safely extract the year from strings or datetime objects
                if int(str(created)[:4]) < 2020:
                    human_files.append(row["text"])
            except (ValueError, TypeError):
                pass
                
        if len(human_files) >= 100:
            break


    human_stats = []
    for text in human_files:
        file_stats = []
        #reader = PdfReader(human_file)
        #text = ""
        #for page in reader.pages:
            #text += page.extract_text()
        
        for measure in all_measures:
            file_stats.append(measure(text))

        human_stats.append(file_stats)

    human_avg_stats = []

    num_files = len(human_stats)
    human_avg_stats = [sum(measure_scores) / num_files for measure_scores in zip(*human_stats)]

    data = [["measure name", "AI papers", "human dataset", "diff", "AI or human"]]

    for i in range(len(all_measures)):
        data.append([all_measures[i].__name__, ai_avg_stats[i], human_avg_stats[i], abs(ai_avg_stats[i] - human_avg_stats[i]), "AI" if ai_avg_stats[i] > human_avg_stats[i] else "human"])

    print(tabulate.tabulate(data, headers="firstrow", tablefmt="fancy_grid"))

    

    
    
