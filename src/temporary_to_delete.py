import pandas as pd
from time import perf_counter

new_tr1 = {"date": "2002-02-22", "amount": 10, "currency": "HUF"}
new_tr2 = {"date": "2002-02-24", "amount": 10, "currency": "USD"}
new_tr3 = {"date": "2002-02-24", "amount": -1, "currency": "HUF"}
new_tr4 = {"date": "2002-02-22", "amount": 10, "currency": "USD"}
new_tr5 = {"date": "2002-02-11", "amount": 10, "currency": "USD"}
new_tr6 = {"date": "2002-02-28", "amount": -1, "currency": "HUF"}

trs = []

def add_tr(transact):
    new_transaction = {"date": transact["date"], transact["currency"]: transact["amount"]}
    new_tr_date = False
    new_tr_currency = False
    if not trs:
        trs.append(new_transaction)
    else:
        for transaction in trs:
            if new_transaction["date"] in transaction["date"]:
                new_tr_date = True
                if transact['currency'] in transaction:
                    new_tr_currency = True
                    break
        if new_tr_currency:
            transaction[transact['currency']] = transaction[transact['currency']] + transact["amount"]
        elif new_tr_date:
            transaction[transact['currency']] = transact["amount"]
        else:
            trs.append(new_transaction)
                # else:
                #     if transact['currency'] not in transaction:
                #         transaction[transact['currency']] = transact["amount"]
            # elif new_transaction["date"] not in transaction["date"]:
            #     trs.append(new_transaction)
t1_start = perf_counter()
# print('0: ', trs)
# add_tr(new_tr1)
# print('1: ', trs)
# add_tr(new_tr2)
# print('2: ', trs)
# add_tr(new_tr3)
# print('3: ', trs)
t1_stop = perf_counter()
# df = pd.DataFrame(index=[new_tr1["date"]])
# # df = df.set_index(["date"]).sort_index()

# df[new_tr1["currency"]] = new_tr1["amount"]

# # for i in range(len(df.index)):
# #     if new_tr["date"] < df.index[i]:
# #         pass

# print(df)

def add_tr2(transact):
    global trs
    new_transaction = {"date": transact["date"], transact["currency"]: transact["amount"]}
    if not trs:
        trs.append(new_transaction)
        return
    dates = [trs[i]['date'] for i in range(len(trs))]
    in_dates, position = _evaluate_transaction_date(transact["date"], dates)

    if position == "min":
        for transaction in trs:
            currencies = []
            for currency in transaction:
                currencies.append(currency)
            if transact["currency"] in currencies:
                 transaction[transact['currency']] = transaction[transact['currency']] + transact["amount"]
            else:
                transaction[transact['currency']] = transact["amount"]
        trs.append(new_transaction)
    elif position == "max":
        transaction_to_add = {}
        transaction_to_add["date"] = transact["date"]
        for transaction in trs:
            if transaction["date"] == max(dates):
                currencies = []
                for item in transaction:
                    if item != "date":
                        currencies.append(item)
                        transaction_to_add[item] = transaction[item]
                if transact["currency"] in currencies:
                    transaction_to_add[transact['currency']] = transaction_to_add[transact['currency']] + transact["amount"]
                else:
                    transaction_to_add[transact['currency']] = transact["amount"]
        trs.append(transaction_to_add)
    elif position == "middle":
        for transaction in trs:
            if transaction["date"] >= transact["date"]:
                currencies = []
                for currency in transaction:
                    currencies.append(currency)
                if transact["currency"] in currencies:
                    transaction[transact['currency']] = transaction[transact['currency']] + transact["amount"]
                else:
                    transaction[transact['currency']] = transact["amount"]
        if not in_dates:
            trs.append(new_transaction)
    trs = sorted(trs, key = lambda i: i["date"])

    
def _evaluate_transaction_date(date, dates):
    in_dates = date in dates
    if dates:
        if date < min(dates):
            position = "min"
        elif date > max(dates):
            position = "max"
        else:
            position = "middle"
    else:
        position = None
    return in_dates, position

t2_start = perf_counter()
print('0: ', trs)
add_tr2(new_tr1)
print('1: ', trs)
add_tr2(new_tr2)
print('2: ', trs)
add_tr2(new_tr3)
print('3: ', trs)
add_tr2(new_tr4)
print('4: ', trs)
add_tr2(new_tr5)
print('5: ', trs)
add_tr2(new_tr6)
print('6: ', trs)
t2_stop = perf_counter()

print("perf1: ", t1_stop - t1_start)
print("perf2: ", t2_stop - t2_start)