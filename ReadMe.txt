demo how to use goes to 'HowTo.txt'

1. parser tested on python2.7, python3 shoudld be modified by yourself. 
2. parser workflow:
  (1) use space number of each line as the hierachy level
  (2) based on space number created XML
  (3) parse XML to dict, each higher level as the key, lower level as the value
  Since (2) needs to parse XML, here we use beautifulsoup4, So you need install the library. Actually it is not necessary, but you need modify it yourself.
3. how to use:
  (1) import lib
    from parseQosOutput import show_cmd_output_analyze
  (2) instatiate it 
    ins = show_cmd_output_analyze(cfg)
  (3) 3 Main func and attributes you might need
    "ins.printDict()" print the whole hierachy level you need, you can also give variable to show less
    "ins.outputDict" get the real value you need
    "ins.exportDict()" export the children dict of the outputDict

