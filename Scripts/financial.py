import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf


def net_present_value(cash_flows: list[float], discount_rate: float, investment:float) -> float:
    npv = sum([cash_flows[i] / math.pow(1 + discount_rate, i + 1) for i in range(len(cash_flows))])
    return npv


def get_investment(down_pay:float, ins_premium:float, hoa:float) -> float:
    return down_pay + ins_premium + hoa


def get_cash_flow(tr:float, tr_growth:float, loan: float, ip:float, ip_growth:float, hoa:float, hoa_g:float, term:int) ->float:
    if term < 1:
        raise Exception('value error: term must be positive integer!')
    else:
        res = tr * math.pow(1 + tr_growth, term - 1) + loan + ip * math.pow(1 + ip_growth, term - 1) + hoa * math.pow(1+ hoa_g, term - 1)
        return res



def NPV_per_unit(property_value_0, property_value_index, popularity_factor, terminal_property_value_growth_rate):
  income_tax_ratio = 0.3
  property_tax_ratio = 0.01
  cost_of_capital = 0.10
  property_value_list = property_value_index
  property_value = [property_value_0 * x for x in property_value_list]
  rental_income = []
  other_income = []
  hoa_fee = []
  mortgage_payment_per_year = []
  insurance_premium = []
  renovation_expense = []
  depreciation_of_renovation = []
  property_tax = []
  utility_expense = []
  maintenence_expense = []
  management_expense = []



  for k in range(len(property_value_list)):
    property_value_list[k] *= property_value_0

    for w in range(len(property_value_list)):

      rental_income.append(property_value[w]*0.05*popularity_factor*12)
      other_income.append(property_value[w]*popularity_factor*0.005)
      hoa_fee.append(property_value[w] * 0.002)
      mortgage_payment_per_year.append((property_value[w]*0.8)*(cost_of_capital/12*(1 + cost_of_capital/12)**360)/((1 + cost_of_capital/12)**360 - 1))
      insurance_premium.append(property_value[w] * 0.003)
      renovation_expense.append(property_value[w] * 0.05)
      depreciation_of_renovation.append(renovation_expense[w]/5)
      property_tax.append(property_value[w] * property_tax_ratio)
      utility_expense.append(rental_income[w] * 0.04)
      maintenence_expense.append(property_value[w] * 0.01)
      management_expense.append(rental_income[w]*0.1)
    
    rental_income[0] = 0
    other_income[0] = 0
    mortgage_payment_per_year[30] = 0
    renovation_expense[1:] = [0] * (len(renovation_expense) - 1)
    depreciation_of_renovation[0] = 0
    depreciation_of_renovation[6:] = np.zeros(len(depreciation_of_renovation[6:]))
    maintenence_expense[0] = 0
    maintenence_expense[1] = 0
    management_expense[0] = 0

    for i in range(len(property_value_list)):
        dcf_list = []
        if i == 0:
          net_income = (-property_value_0 * 0.2 - hoa_fee[i] - insurance_premium[i] - renovation_expense[i] - property_tax[i] - utility_expense[i])
          dcf = net_income
          dcf_list.append(dcf)
        elif i == 1:
          net_income = (rental_income[i] + other_income[i] - hoa_fee[i] - insurance_premium[i] - mortgage_payment_per_year[i] - renovation_expense[i] - depreciation_of_renovation[i] - property_tax[i] - utility_expense[i] - management_expense[i])*(1-income_tax_ratio)
          dcf = depreciation_of_renovation[i] + net_income
          dcf_list.append(dcf)
        elif i > 1 and i < 6:
          net_income = (rental_income[i] + other_income[i] - hoa_fee[i] - insurance_premium[i] - mortgage_payment_per_year[i] - renovation_expense[i] - depreciation_of_renovation[i] - property_tax[i] - utility_expense[i] - maintenence_expense[i] - management_expense[i])*(1-income_tax_ratio)
          dcf = depreciation_of_renovation[i] + net_income
          dcf_list.append(dcf)
        elif i > 5 and i < 30:
          net_income = (rental_income[i] + other_income[i] - hoa_fee[i] - insurance_premium[i] - mortgage_payment_per_year[i] - property_tax[i] - utility_expense[i] - maintenence_expense[i] - management_expense[i])*(1-income_tax_ratio)
          dcf = net_income
          dcf_list.append(dcf)
        else:
          net_income = (rental_income[i] + other_income[i] - hoa_fee[i] - property_tax[i] - utility_expense[i] - maintenence_expense[i] - management_expense[i])*(1-income_tax_ratio)
          dcf = depreciation_of_renovation[i] + net_income
          dcf = dcf + dcf*(1+terminal_property_value_growth_rate)/(cost_of_capital-terminal_property_value_growth_rate)
          dcf_list.append(dcf)
      
    discount_rate = cost_of_capital
    cash_flows = dcf_list
    npv = npf.npv(discount_rate, cash_flows)
  return npv