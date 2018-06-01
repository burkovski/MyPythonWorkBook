def scanner(name, function):
    for line in open(name):
        function(line)