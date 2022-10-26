from time import sleep
import yfinance as yf
import pyautogui as pg
import datetime
from math import atan
import pandas as pd

Total_investment = 1000
TIPD = 30
TIPD_E = 20
Taxes = 7.5
Tolerance = -40


def getRTQ_IN(i):
    Company = "ZEEL"
    data = yf.download(tickers=f"{Company}.NS", period="1d", interval="1m")
    Price = float((data.iloc[i, 1] + data.iloc[i, 2] + data.iloc[i, 3] + data.iloc[i, 0]) * 0.25)
    Volume = float(data.iloc[i, 5])
    return Price, Volume


def getRTQ_US(i):
    Company = "RIOT"
    data = yf.download(tickers=f"{Company}", period="1d", interval="1m")
    Price = float((data.iloc[i, 1] + data.iloc[i, 2] + data.iloc[i, 3] + data.iloc[i, 0]) * 0.25)
    Volume = float(data.iloc[i, 5])
    return Price, Volume


def getPred(arr):
    N = len(arr) - 2
    i = 0
    sum = 0
    while i <= N:
        if arr[i] > arr[i + 1]:
            sum = sum + (5 - i)
        elif arr[i] < arr[i + 1]:
            sum = sum - (5 - i)
        else:
            sum = sum + 0
        i = i + 1

    slope = atan((arr[0] + arr[N + 1]) / 10) * (180 / 3.14)
    n1 = slope / abs(slope)
    n2 = sum / abs(sum)
    print(slope)
    if n1 == n2:
        return sum, 1
    else:
        return sum, 0


def getPrAct(i):
    t1 = i - 10
    share_CP11, Volume1 = getRTQ_IN(t1 - 1)
    sum1 = 0
    while t1 <= i:
        share_CP, Volume = getRTQ_IN(t1)
        if share_CP > share_CP11:
            sum1 = sum1 + 1
        elif share_CP < share_CP11:
            sum1 = sum1 - 1
        else:
            sum1 = sum1
        share_CP11 = share_CP
        t1 = t1 + 1
    return sum1


def Buy(share_SN):
    pg.moveTo(1280, 369)
    pg.click()
    pg.moveTo(1519, 477)
    pg.click()
    pg.write(share_SN)
    pg.moveTo(1322, 779)
    pg.click()


def Sell(share_SN):
    share_SN = abs(share_SN)
    pg.moveTo(1379, 365)
    pg.click()
    pg.moveTo(1519, 477)
    pg.click()
    pg.write(share_SN)
    pg.moveTo(1322, 779)
    pg.click()


Balance = Total_investment * 5  # Using leverage of 5x 
Trigger_Bal = 0
share_BP = 0  # share buy price
share_SP = 0  # share sell price
share_SN = 0  # Total no of shares bought/short sell
Est_Profit = 0
Est_Profit1 = 0
sigmaVOl1 = 0
VWAP1 = 0    # VWAP means Volume Weighted Average Price
VWAP2 = 0
VWAP3 = 0
VWAP4 = 0
VWAP5 = 0
VWAP6 = 0
VWAP7 = 0
VWAP8 = 0
VWAP9 = 0
VWAP10 = 0
t = 0
starttime = 556
starti = 15
endi = 355
i = 5
hour = datetime.datetime.now().hour * 60
minute = datetime.datetime.now().minute + hour
current_time = datetime.datetime.now()
if minute < starttime:
    print(f"Sleeping, you are {starttime - minute} minutes early")
    sleep((starttime - minute) * 60)

while i <= endi:
    share_CP, Volume = getRTQ_IN(i)
    sigmaVOl = sigmaVOl1 + Volume
    VWAP = (sigmaVOl1 * VWAP1 + Volume * share_CP) / sigmaVOl
    slope_1 = VWAP - VWAP5
    slope_2 = VWAP1 - VWAP6
    slope_3 = VWAP2 - VWAP7
    slope_4 = VWAP3 - VWAP8
    slope_5 = VWAP4 - VWAP9
    slope_6 = VWAP5 - VWAP10
    if i >= starti:
        arr_pG = [slope_1, slope_2, slope_3, slope_4, slope_5, slope_6]
        resultG, Val = getPred(arr_pG)
        Price_Act = getPrAct(i)
        if (resultG == -15 and Val == 1) and Price_Act == -5 and t == 0:
            if share_SN > 0:
                Balance = share_SN * share_BP + (Est_Profit - Taxes) * 5 + Balance
                share_SN = 0
                print(Balance)

            SN = -int(Balance / share_CP)
            if SN != 0:
                Balance = Balance + (SN * share_CP)
                share_BP = (share_CP * SN + share_SN * share_BP) / (SN + share_SN)
                share_SN = SN + share_SN

        elif (resultG == 15 and Val == 1) and Price_Act == 5 and t == 0:
            if share_SN < 0:
                Balance = (-share_SN * share_BP) + (Est_Profit - Taxes) * 5 + Balance
                share_SN = 0
                print(Balance)

            SN = int(Balance / share_CP)
            if SN != 0:
                Balance = Balance - (SN * share_CP)
                share_BP = (share_CP * SN + share_SN * share_BP) / (SN + share_SN)
                share_SN = SN + share_SN

        Est_Profit = (share_CP - share_BP) * share_SN
        Trigger_Bal = (Balance + abs(share_SN) * share_BP) / 5 + (Est_Profit - Taxes) - Total_investment

        if i == endi:
            Balance = Balance + abs(share_SN) * share_BP + (Est_Profit - Taxes) * 5
            share_SN = 0

        elif Trigger_Bal >= TIPD and Est_Profit < TIPD_E:
            print("--------------------------")
            print(current_time)
            print(f"shares: {share_SN}")
            print(f"Est profit:{Est_Profit}")
            print(f"Balance:{Balance / 5}")
            print(f"Porfolio Value:{Trigger_Bal + Total_investment}")
            print(f"Increasing or decreasing:{resultG}")
            print(f"Delta: {share_CP - share_BP}")
            print(f"VWAP Value:{VWAP}")
            print(f"share_BP:{share_BP}")
            print(f"share_CP:{share_CP}")
            break

        elif Est_Profit <= Tolerance:
            Balance = Balance + abs(share_SN) * share_BP + (Est_Profit - Taxes) * 5
            share_SN = 0
            share_BP = 0

        elif Est_Profit > TIPD_E:
            t = 1
            TIPD = 100
            if (Est_Profit < Est_Profit1 - 3) and share_SN != 0:
                Balance = Balance + abs(share_SN) * share_BP + (Est_Profit - Taxes) * 5
                share_SN = 0
                share_BP = 0
            if Trigger_Bal >= 100:
                print("--------------------------")
                print(f"shares: {share_SN}")
                print(f"Est profit:{Est_Profit}")
                print(f"Balance:{Balance / 5}")
                print(f"Porfolio Value:{Trigger_Bal + Total_investment}")
                print(f"Increasing or decreasing:{resultG}")
                print(f"Delta: {share_CP - share_BP}")
                print(f"VWAP Value:{VWAP}")
                print(f"share_BP:{share_BP}")
                print(f"share_CP:{share_CP}")
                break

        elif Est_Profit <= TIPD_E:
            t = 0
            TIPD = 30

        print("--------------------------")
        print(datetime.datetime.now())
        print(f"shares: {share_SN}")
        print(f"Est profit:{Est_Profit}")
        print(f"Balance:{Balance / 5}")
        print(f"Porfolio Value:{Trigger_Bal + Total_investment}")
        print(f"Increasing or decreasing:{resultG}")
        print(f"Delta: {share_CP - share_BP}")
        print(f"VWAP Value:{VWAP}")
        print(f"share_BP:{share_BP}")
        print(f"share_CP:{share_CP}")
    sigmaVOl1 = sigmaVOl
    VWAP10 = VWAP9
    VWAP9 = VWAP8
    VWAP8 = VWAP7
    VWAP7 = VWAP6
    VWAP6 = VWAP5
    VWAP5 = VWAP4
    VWAP4 = VWAP3
    VWAP3 = VWAP2
    VWAP2 = VWAP1
    VWAP1 = VWAP
    Est_Profit1 = Est_Profit
    i = i + 1
    if i >= 16:
        sleep(55)

print(i)
print(f"Net Profit:{Trigger_Bal}")
