# Save data in memory
def save_in_memory(file, document):
    f=open(file,'a')
    f.write(str(document))
    f.close