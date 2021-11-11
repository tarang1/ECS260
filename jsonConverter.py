import json

def dump_json(d, fil) :
    out_file = open(fil, "w")
      
    json.dump(d, out_file, indent = 4)
      
    out_file.close()
    
    
    
def get_dump(fil) :
    # json.load(_io)
    io = open("drive/Shareddrives/ECS 260/sample_data.json","r")

    return json.load(io)
