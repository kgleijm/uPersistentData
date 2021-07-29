
import json

# "abstract" class to encapsulate variables and manage persistence by keeping a record on file
class Pdp:

    # static dict keeping track of all Pdp values's
    persistentData = dict()

    def __init__(self, publicName, value):
        self.load()
        self.publicName = publicName
        self.verify(self.getdefault())
        if not self.set(value):
            print("Error, initial value of", publicName, " does not pass validation")
            self.set(self.getdefault())

    # Overridable method where childClasses can verify their input data
    def verify(self, value):
        raise NotImplementedError

    # Returns a default when no initial value is supplied
    def getdefault(self):
        raise NotImplementedError

    # Static "private" method to sync dictionary of values with record on file
    @staticmethod
    def save():
        with open("persistentData.json", "w") as f:
            json.dump(Pdp.persistentData, f)
            print("Pdp.save() saved persistent data")

    # Static "private" method to sync dictionary of values with record on file
    @staticmethod
    def load():
        try:
            with open("persistentData.json", "r") as f:
                Pdp.persistentData = json.load(f)
                print("Opened file with load():", Pdp.persistentData)
        except:
            print("persistentData.json does not exist, creating file with Pdp.save()")
            Pdp.save()

    # Static method that clears out all data
    @staticmethod
    def reset():
        Pdp.persistentData = dict()
        try:
            with open("persistentData.json", "r+") as f:
                f.truncate()
                Pdp.save()
        except:
            print()

    # Set value to input with forced Verification
    def set(self, value):
        if self.verify(value):
            Pdp.persistentData[self.publicName] = value
            print(self.publicName, "set to value:", value)
            Pdp.save()
            return True
        return False

    # Get value
    def get(self):
        return Pdp.persistentData[self.publicName]


class PdpString(Pdp):

    def __init__(self, publicName, value, maxLength):
        self.maxLength = maxLength
        self.PdpType = "stringPdp"
        super().__init__(publicName, value)

    def getdefault(self):
        return ""

    def verify(self, value):
        return isinstance(value, str) and len(value) <= self.maxLength




class PdpConfig(Pdp):

    def __init__(self, publicName, value):
        super().__init__(publicName, value)
        self.getCommunicationRepresentation()
        self.configType = "percentConfig"

    def getCommunicationRepresentation(self):
        raise NotImplementedError


class PdpPercent(Pdp):

    def __init__(self, publicName, value):
        super().__init__(publicName, value)
        self.PdpType = "percent"

    def getdefault(self):
        return 0

    def verify(self, value):
        try:
            return 0 <= value <= 100
        except:
            return False





PdpString.reset()



test = PdpPercent("TestPercent", 103)
testString = PdpString("TestString", "Super Cool String", 100)


test.set(25)


test.set("asdasd")

print("Got from get()", test.get())

print("Sucessfully ran script")

    # Pdp stands for persistent dataPoint and is a variable that stores its data in persistent memory using jsons



#
# class A:
#     def __init__(self, msg):
#         print("Class A constructor with msg:", msg)
#
# class B(A):
#     def __init__(self, msg):
#         super().__init__(msg)
#         print("Class B constructor")
#
# b = B("Yo")

# import json
#
# data = dict()
#
# data["0"] = "yes"
# data["1"] = True
# data["2"] = 0
#
#
# with open("persistentData.json", "w") as f:
#     json.dump(data, f)
#
# with open("persistentData.json", "r") as f:
#     data2 = json.load(f)
#     print("0:", data2["0"])
#     print("1:", data2["1"])
#     print("2:", data2["2"])
