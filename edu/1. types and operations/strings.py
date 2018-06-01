import sys


S = "Spam, eggs, two words"  # Методы строк
print(S.find("two"))
print(S.replace("pam", "TRING!"))
print(S.split(", "))
print(S.upper())
print(S.isalpha())
S = ' ' + S
print(S)
S = S.strip()
print(S)

S = "StrSPAMingSPAM.SPAM"
S = S.replace("SPAM", "")
L = list(S)
L[-1] = '!'
S = ''.join(L)
print(S)
S = "Bob Jack Arnold Alex"
L = S.split()
print(L)
L[0] = "Fredie"
S = ' '.join(L)
print(S)


print("That is %d %s bird!" % (1, "dead"))  # Выражение форматирования
x = 1234
res = "integers: ...%d...%-6d...%06d" % (x, x, x)
print(res)

x = 1.23456789
res = "%e | %f | %g" % (x, x, x)
print(res)

res = "%-6.2f | %06.2f | %+06.2f" % (x, x, x)
print(res)

res = "%f | %.2f | %*f" % (x, x, 4, x)
print(res)

print("%(n)d %(x)s" % {"n": 1, "x": "one"})

reply = """
Greetings...
Hello %(name)s!
Your age squared is %(age)d
"""
values = {'name': 'Bob', 'age': 42}
print(reply % values)
print(vars())
print("Directory: %(__file__)s" % vars())
print("Names: %(S)s" % vars())


template = "{0}, {1} and {2}"  # Метод форматирования
print(template.format("spam", "ham", "eggs"))

template = "{motto}, {pork} and {food}"
print(template.format(motto='spam', pork='ham', food='eggs'))

template = "{motto}, {0} and {food}"
print(template.format('ham', motto='spam', food='eggs'))
print(template.format(42, motto=3.14, food=[1, 2]))

print("My {1[spam]} runs {0.platform}".format(sys, {"spam": "laptop"}))
print("My {config[spam]} runs {sys.platform}".format(sys=sys, config={"spam": "laptop"}))

print("Directory: {0[__file__]}".format(vars()))
print("Names: {0[S]}".format(vars()))

somelist = list("spam")
print("First: {0[0]}, third: {0[2]}".format(somelist))
print("First: {0}, last: {1}".format(somelist[0], somelist[-1]))
parts = (somelist[0], somelist[-1], somelist[1:3])
print("First: {0}, middle{2}, last: {1}".format(*parts))

print("{0:10} = {1:10}".format("spam", 123.4567))
print("{0:>10} = {1:<10}".format("spam", 123.4567))
print("My {1[item]:>10} runs {0.platform:>10}".format(sys, dict(item="laptop")))

data = dict(platform=sys.platform, spam='device')
print("My {spam} runs {platform}".format(**data))
print("My %(spam)s runs %(platform)s" % data)
