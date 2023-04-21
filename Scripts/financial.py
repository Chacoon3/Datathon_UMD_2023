import math


def net_present_value(cash_flow: list[float], discount_rate: float, investment:float) -> float:
    npv = sum([cash_flow[i] / math.pow(1 + discount_rate, i + 1) for i in range(len(cash_flow))])
    return npv


def get_investment(down_pay:float, ins_premium:float, hoa:float) -> float:
    return down_pay + ins_premium + hoa


def get_cash_flow(tr:float, tr_growth:float, loan: float, ip:float, ip_growth:float, hoa:float, hoa_g:float, term:int) ->float:
    if term < 1:
        raise Exception('value error: term must be positive integer!')
    else:
        res = tr * math.pow(1 + tr_growth, term - 1) + loan + ip * math.pow(1 + ip_growth, term - 1) + hoa * math.pow(1+ hoa_g, term - 1)
        return res
