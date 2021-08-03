import json


# "abstract" class to encapsulate variables and manage persistence by keeping a record on file
class Pdp:
    # static dict keeping track of all Pdp values's
    persistentData = dict()

    def __init__(self, publicName, value):

        # Read values from record on file
        self.load()

        # Initiate record keeping in working memory
        # Simulate abstraction by calling a nonexistent function
        self.publicName = publicName
        self.verify(self.getDefault())

        if self.publicName in Pdp.persistentData:
            print("value for", publicName, "already exists, loaded:", self.get())
        elif not self.set(value):
            print("Error, initial value of", publicName, " does not pass validation")
            self.set(self.getDefault())

    # Overridable method where childClasses can verify their input data
    def verify(self, value):
        raise NotImplementedError

    # Returns a default when no initial value is supplied
    def getDefault(self):
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
        super().__init__(publicName, value)

    def getDefault(self):
        return ""

    def verify(self, value):
        return isinstance(value, str) and len(value) <= self.maxLength


class PdpNumeric(Pdp):

    def __init__(self, publicName, value):
        super().__init__(publicName, value)

    def getDefault(self):
        return 0

    def verify(self, value):
        # microPython does not support isnumeric().
        # Trying to add a non numeric value to an int will cause an exception thus returning false
        try:
            1 + value
            return True
        except:
            return False


# Configs are the type of persistent dataPoints communicated and possibly altered by a remote device
class Config(Pdp):

    def get(self):
        return self.data["Value"]

    def __init__(self, publicName, value, mutable):
        self.configType = "Config base"
        self.mutable = mutable
        # self.getCommunicationRepresentation()
        super().__init__("Conf_" + publicName, value)
        self.data = {"Type": self.getType(), "Name": self.publicName, "Value": self.get(), "Mutable": self.mutable}


    def getCommunicationRepresentation(self):
        return {"Type": self.getType(), "Name": self.publicName, "Value": self.get(), "Mutable": self.mutable}

    def update(self, newRepresentation):

        if self.mutable:
            try:
                return self.set(newRepresentation["Value"])
            except:
                print("Unexpected error at update of ", self.publicName)
                return False
        else:
            print("Unexpected operation,", self.publicName, "tried to mutate but is immutable")

    def getType(self):
        raise NotImplementedError


class ConfigPercent(Config):

    def __init__(self, publicName, value, mutable):
        super().__init__(publicName, value, mutable)

    def getDefault(self):
        return 0

    def verify(self, value):
        try:
            return 0 <= value <= 100
        except:
            return False

    def getType(self):
        return "Percent"


Pdp.reset()

testNumeric = PdpNumeric("TestNumeric", "asdasd")
testNumeric.set("äsdasdas")
testNumeric.set(78)

testPercConf = ConfigPercent("TestPercConf", 15, True)

print(testPercConf.getCommunicationRepresentation())
testPercConf.update({'Type': 'Percent', 'Name': 'Conf_TestPercConf', 'Value': 77, 'Mutable': True})
print(testPercConf.getCommunicationRepresentation())

print("Sucessfully ran script")
