from enum import Enum


COI = Enum("COI", ["CONSULT", "BANK", "CLOTHING", "HARDWARE"])


class Company:
    def __init__(self, name, company_id, COI):
        self.COI = COI
        self.name = name
        self.id = company_id


class User:
    def __init__(self, name, user_id, role):
        self.name = name
        self.id = user_id
        self.role = role
        self.COI_read = set()
        self.company_ids = set()
        self.whitelist = set()

    def registerCompany(self, company):
        self.COI_read.add(company.COI)
        self.company_ids.add(company.id)


class File:
    def __init__(self, path, company_id, file_id, sanitized):
        self.company_id = company_id
        self.path = path
        self.id = file_id
        self.sanitized = sanitized


class ChineseWall:
    def __init__(self):
        self.companies = {}
        self.company_name_to_companyid = {}
        self.file_name_to_fileid = {}
        self.users = {}
        self.files = {}
        pass

    def addCompany(self, name, COI):
        new_company = Company(name, name, COI)
        self.companies[name] = new_company
        self.company_name_to_companyid[name] = name
        return name

    def addUser(self, name, role, companies):
        new_user = User(name, name, role)
        self.users[name] = new_user
        for x in companies:
            new_user.whitelist.add(self.companies[self.company_name_to_companyid[x]].id)
        return name

    def addFile(self, path, company_id, sanitized):
        new_file = File(path, company_id, path, sanitized)
        self.files[path] = new_file
        self.file_name_to_fileid[path] = path
        return path

    def requestRead(self, user, file):
        file_comp = self.companies[file.company_id]

        if file.sanitized:
            # no need to register read -- public information
            return True

        if not file_comp.id in user.whitelist:
            return False
        if file_comp.id in user.company_ids:
            # need to register read since information is privileged
            user.registerCompany(file_comp)
            return True

        if file_comp.COI in user.COI_read:
            return False

        # need to register read since information is privileged
        user.registerCompany(file_comp)
        return True

    def requestWrite(self, user, file):
        if self.requestRead(user, file) and len(user.company_ids) == 1:
            return True
        return False


if __name__ == "__main__":
    CW = ChineseWall()

    acme_id = CW.addCompany("acme", COI.CONSULT)
    zift_id = CW.addCompany("zift", COI.CONSULT)
    mQuess_id = CW.addCompany("mQuess", COI.CONSULT)
    adp_id = CW.addCompany("adp", COI.CONSULT)
    boi_id = CW.addCompany("boi", COI.BANK)
    bob_id = CW.addCompany("bob", COI.BANK)
    bom_id = CW.addCompany("bom", COI.BANK)
    cb_id = CW.addCompany("cb", COI.BANK)
    nike_id = CW.addCompany("nike", COI.CLOTHING)
    adidas_id = CW.addCompany("adidas", COI.CLOTHING)
    puma_id = CW.addCompany("puma", COI.CLOTHING)
    fila_id = CW.addCompany("fila", COI.CLOTHING)
    apple_id = CW.addCompany("apple", COI.HARDWARE)
    samsung_id = CW.addCompany("samsung", COI.HARDWARE)
    sony_id = CW.addCompany("sony", COI.HARDWARE)

    filea_id = CW.addFile("a", acme_id, 0)
    fileb_id = CW.addFile("b", boi_id, 0)
    filec_id = CW.addFile("c", zift_id, 0)

    user1_id = CW.addUser("1", "hr", [])

    resp = CW.requestRead(CW.users[user1_id], CW.files[filea_id])
    print(resp)
    resp = CW.requestRead(CW.users[user1_id], CW.files[filec_id])
    print(resp)
    resp = CW.requestRead(CW.users[user1_id], CW.files[fileb_id])
    print(resp)
    resp = CW.requestRead(CW.users[user1_id], CW.files[filea_id])
    print(resp)
