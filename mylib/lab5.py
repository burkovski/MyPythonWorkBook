class BankAccountError(Exception):
    def __init__(self, msg):
        self.res = "BankAccountError"
        self.res += ": <{0}>".format(', '.join(msg))


class BankAccount:
    ba_numbers = set()
    def __init__(self, num, sum, per, daily_max, min_sum):
        try:
            BankAccount.ba_checker(num, sum, per)
        except BankAccountError as exc:
            print(exc.res)
        else:
            BankAccount.ba_numbers.add(num)
            self.ba_number = num
            self.ba_sum = sum
            self.ba_percents = per
            self.ba_daily_max = daily_max
            self.ba_min_sum = min_sum

    @staticmethod
    def ba_checker(num=None, sum=None, per=0):
        msg = []
        if num in BankAccount.ba_numbers:
            msg.append("account number must be unique")
        if sum is None:
            msg.append("must be transferred sum")
        if not 0 <= per <= 100:
            msg.append("percent must be between 0 and 100")
        if msg:
            raise BankAccountError(msg)

    def giveSurcharge(self):
        new_sum = self.ba_sum * (self.ba_percents / 100)
        self.ba_sum += new_sum

    def ba_getData(self):
        res = ("| Number: {0:09}\n"
               "| Sum: {1:.2f}$\n"
               "| Percents: {2:.1f}%\n".format(
                self.ba_number,
                self.ba_sum,
                self.ba_percents))
        return res

    def _putMoney(self, value):
        self.ba_sum += value

    def _getMoney(self, value):
        msg = []
        if value > self.ba_sum:
            msg.append("not enough mooney for transaction")
        if value > self.ba_daily_max:
            msg.append("exceeded daily limit")
        if self.ba_min_sum > self.ba_sum - value:
            msg.append("exceeded minimal sum")
        if msg:
            raise BankAccountError(msg)
        else:
            self.ba_sum -= value

    def newPercents(self, new_per):
        try:
            BankAccount.ba_checker(sum=self.ba_sum, per=new_per)
        except BankAccountError as exc:
            print(exc.res)
        else:
            self.ba_percents = new_per


class Depositor:
    def __init__(self, name, ID, password):
        self.dep_id = ID
        self.dep_name = ' '.join(name.split()[:-1])
        self.dep_surname = name.split()[-1]
        self.dep_password = password

    def dep_getData(self):
        res = ("| User ID: {0}\n"
               "| Name: {1}\n"
               "| Surname: {2}\n".format(
                self.dep_id,
                self.dep_name,
                self.dep_surname))
        return res


class DepositorBankAccount(BankAccount, Depositor):
    def __init__(self, name, ID, password, num, sum, per, d_max, s_min):
        Depositor.__init__(self, name, ID, password)
        try:
            BankAccount.__init__(self, num, sum, per, d_max, s_min)
        except BankAccountError as exc:
            print(exc.res)

    def check_password(self, password):
        if password == self.dep_password:
            return True
        else:
            print("Wrong password!")

    def getData(self, password):
        if self.check_password(password):
            sepline = '-' * 20
            res = self.dep_getData()
            res += self.ba_getData()
            print("+{0}\n{1}{2}+{0}".format(
                   sepline,
                   self.dep_getData(),
                   self.ba_getData()))

    def getMoney(self, password, value):
        if self.check_password(password):
            try:
                BankAccount._getMoney(self, value)
            except BankAccountError as exc:
                print(exc.res)

    def putMoney(self, password, value):
        if self.check_password(password):
            BankAccount._putMoney(self, value)

    def changePassword(self, old_password, new_password):
        if self.check_password(old_password):
            self.dep_password = new_password


if __name__ == "__main__":
    X = DepositorBankAccount("Bob Smith Jones", "FC12345", "spameggs", 111, 50000, 15, 10000, 1000)
    X.getData("spameggs")
    X.getMoney("spameggs", 499999)
    X.putMoney("spameggs", 20000)
    X.newPercents(10)
    X.giveSurcharge()
    X.changePassword("spameggs", "eggsspam")
    X.getData("eggsspam")
    X.getMoney("eggsspam", 7000)
    X.getData("eggsspam")